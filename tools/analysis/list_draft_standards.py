#!/usr/bin/env python3
"""List all standards documents in standards/src/ whose front-matter tags include `status/draft`.
Outputs a simple newline-separated list to stdout and writes a CSV report in tools/reports/.
Usage:
    python tools/analysis/list_draft_standards.py [--csv]
"""
from pathlib import Path
import re
import argparse
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]  # tools/analysis/ -> repository root
SRC_DIR = ROOT / 'standards' / 'src'
REPORT_DIR = ROOT / 'tools' / 'reports'

FM_BOUNDARY = re.compile(r'^---\s*$')
DRAFT_PATTERN = re.compile(r'^\s*-\s*status/draft\s*$', re.IGNORECASE)

def is_draft(md_path: Path) -> bool:
    try:
        text = md_path.read_text(encoding='utf-8').splitlines()
    except Exception:
        return False
    if not text or text[0].strip() != '---':
        return False
    # find end of front-matter
    for i in range(1, len(text)):
        if FM_BOUNDARY.match(text[i]):
            frontmatter = text[1:i]
            break
    else:
        return False
    return any(DRAFT_PATTERN.match(line) for line in frontmatter)

def gather_drafts():
    md_files = sorted(SRC_DIR.glob('*.md'))
    return [p for p in md_files if is_draft(p)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', action='store_true', help='Write CSV report instead of MD')
    args = parser.parse_args()

    drafts = gather_drafts()
    for p in drafts:
        print(p.relative_to(ROOT))

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M')
    if args.csv:
        out_path = REPORT_DIR / f'draft-standards-{timestamp}.csv'
        out_path.write_text('\n'.join(str(p.relative_to(ROOT)) for p in drafts), encoding='utf-8')
    else:
        out_path = REPORT_DIR / f'draft-standards-{timestamp}.txt'
        out_path.write_text('\n'.join(str(p.relative_to(ROOT)) for p in drafts), encoding='utf-8')
    print(f'Report written to: {out_path.relative_to(ROOT)}')
    print(f'Total draft standards: {len(drafts)}')

if __name__ == '__main__':
    main() 