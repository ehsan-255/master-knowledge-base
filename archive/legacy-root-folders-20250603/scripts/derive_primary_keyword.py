#!/usr/bin/env python3
"""derive_primary_keyword.py

Derive a deterministic PRIMARY_TOPIC_KEYWORD for every Markdown file
in a knowledge‑base directory, following the rules in
`drafts/proposal-primary-keywords.md` (Revision 2).

Outputs a CSV mapping (path,current_filename,proposed_keyword) and
reports any raw collisions before disambiguation.

Usage
-----
$ python derive_primary_keyword.py /path/to/master-knowledge-base \
    --out mapping.csv

If no directory is given, the current working directory is scanned.

The script requires Python 3.8+. PyYAML is optional; if unavailable we
fall back to a simple front‑matter parser that only extracts the `title`
key.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # fallback to naive parser later

# ---------------------------------------------------------------------------
# Constants – mirror the proposal, Revision 2
# ---------------------------------------------------------------------------

PREFIXES: List[str] = [
    "standard:",
    "collection:",
    "guide:",
    "overview:",
    "kb definition:",
    "glossary of",
    "universal knowledge base standards - ",
]

ID_SUFFIX_RE = re.compile(r"\s*\([A-Za-z]+-[A-Za-z0-9-]+-[0-9]+\)\s*$", re.IGNORECASE)

STOP_WORDS: set[str] = {
    "a","an","the","is","are","was","were","be","being","been","and","or","but","if","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now",
}

# Pattern for COL‑, GUIDE‑, etc.
COL_RE = re.compile(r"^COL-(.+)\.md$", re.IGNORECASE)
GUIDE_RE = re.compile(r"^GUIDE-(.+)\.md$", re.IGNORECASE)
KB_PREFIX_RE = re.compile(r"^(U|M|D|O|R)-[A-Z0-9-]+-[0-9]+\.md$", re.IGNORECASE)

NOT_ALLOWED = re.compile(r"[^A-Za-z0-9-]")
MULTI_SPACE = re.compile(r"\s+")
MULTI_HYPHEN = re.compile(r"-{2,}")

# ---------------------------------------------------------------------------
# YAML / Front‑matter helpers
# ---------------------------------------------------------------------------

def _extract_yaml_frontmatter(text: str) -> str | None:
    """Return YAML front‑matter block if present, else None."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end]
    return None

def extract_yaml_title(path: Path) -> Optional[str]:
    """Extract the `title` field from YAML front‑matter, if any."""
    try:
        with path.open("r", encoding="utf-8") as f:
            first_chunk = f.read(8192)  # read enough for front‑matter
    except UnicodeDecodeError:
        return None

    block = _extract_yaml_frontmatter(first_chunk)
    if block is None:
        return None

    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict):
                title = data.get("title")
                return str(title) if title is not None else None
        except yaml.YAMLError:
            pass  # fallthrough to naive parse

    # naive parse: look for "title:" at start of line
    for line in block.splitlines():
        if line.lower().startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None

# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def derive_primary_keyword(filename: str, yaml_title: Optional[str]) -> str:
    """Return the PRIMARY_TOPIC_KEYWORD per the proposal."""

    # Step 2 – base‑string selection
    base: str
    if (m := COL_RE.match(filename)):
        base = m.group(1)
    elif (m := GUIDE_RE.match(filename)):
        base = m.group(1)
    elif KB_PREFIX_RE.match(filename):
        base = yaml_title or filename.rsplit(".", 1)[0]
    else:
        base = yaml_title or filename.rsplit(".", 1)[0]

    # Step 3.a – strip prefixes
    b_lower = base.lower()
    for pref in PREFIXES:
        if b_lower.startswith(pref):
            base = base[len(pref):].lstrip()
            break

    # Step 3.a.ii – strip ID suffix
    base = ID_SUFFIX_RE.sub("", base).strip()

    # Step 3.c – non‑allowed chars to space
    base = NOT_ALLOWED.sub(" ", base)
    base = MULTI_SPACE.sub(" ", base).strip()

    # Step 3.d/e/f – tokenize, drop stop‑words, rejoin
    tokens = [tok for tok in base.split(" ") if tok]
    filtered: List[str] = [t for t in tokens if t.lower() not in STOP_WORDS]
    joined = "-".join(filtered)

    # Step 3.i – uppercase + cleanup
    keyword = joined.upper()
    keyword = MULTI_HYPHEN.sub("-", keyword).strip("-")
    if not keyword:
        keyword = "UNTITLED-TOPIC"
    if not re.fullmatch(r"[A-Z0-9]+(-[A-Z0-9]+)*", keyword):
        raise ValueError(f"Derived keyword '{keyword}' from '{filename}' violates character whitelist")
    return keyword

# ---------------------------------------------------------------------------
# File scanning & collision detection
# ---------------------------------------------------------------------------

def scan_markdown_files(root: Path) -> Tuple[List[Tuple[str, str, str]], Dict[str, List[str]]]:
    """Walk `root` and return list of (rel_path, filename, keyword) plus collision map."""

    mapping: List[Tuple[str, str, str]] = []
    collisions: Dict[str, List[str]] = {}

    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        keyword = derive_primary_keyword(path.name, extract_yaml_title(path))
        mapping.append((rel, path.name, keyword))
        collisions.setdefault(keyword, []).append(rel)

    # keep only those with >1 file per keyword
    collisions = {k: v for k, v in collisions.items() if len(v) > 1}
    return mapping, collisions

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Derive PRIMARY_TOPIC_KEYWORDs for Markdown files")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan (default: cwd)")
    parser.add_argument("--out", "-o", type=str, help="Write CSV mapping to this path")
    args = parser.parse_args(argv)

    root_path = Path(args.root).expanduser().resolve()
    if not root_path.is_dir():
        sys.exit(f"error: '{root_path}' is not a directory")

    mapping, collisions = scan_markdown_files(root_path)

    # write CSV if requested
    if args.out:
        out_path = Path(args.out).expanduser()
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["relative_path", "current_filename", "proposed_keyword"])
            writer.writerows(mapping)
        print(f"CSV written to {out_path}")

    # Console summary
    print(f"Scanned {len(mapping)} markdown files under {root_path}.")
    if collisions:
        print("\nRAW COLLISIONS (before -ALT disambiguation):")
        for kw, files in collisions.items():
            print(f"  {kw}: {', '.join(files)}")
    else:
        print("No raw collisions detected.")

if __name__ == "__main__":
    main()
