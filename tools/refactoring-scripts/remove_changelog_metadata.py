#!/usr/bin/env python3
"""
Script to remove the `change_log_url` key from YAML frontmatter of markdown
standards. Conforms to Audit Remediation Initiative SL2 requirements.
- Supports --dry-run (preview modifications)
- Generates timestamped log in tools/reports/
Usage examples:
  python tools/refactoring-scripts/remove_changelog_metadata.py --dry-run
  python tools/refactoring-scripts/remove_changelog_metadata.py
"""

import argparse
import os
from pathlib import Path
from datetime import datetime, timezone
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent  # repository root
STANDARDS_DIR = ROOT_DIR / 'standards' / 'src'


def strip_change_log(content: str):
    """Return new content with change_log_url line removed from frontmatter.
    If key not present, returns original content.
    """
    if not content.startswith('---'):
        return content, False
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, False
    _, frontmatter, rest = parts[0], parts[1], parts[2]
    lines = frontmatter.splitlines()
    new_lines = []
    removed = False
    for line in lines:
        if line.strip().startswith('change_log_url:'):
            removed = True
            continue
        new_lines.append(line)
    if not removed:
        return content, False
    new_frontmatter = '\n'.join(new_lines)
    # Ensure frontmatter ends with newline
    new_content = '---\n' + new_frontmatter + '\n---' + rest
    # Preserve original ending newline if present
    return new_content, True


def process_file(md_file: Path, dry_run: bool, log_lines: list):
    text = md_file.read_text(encoding='utf-8')
    new_text, changed = strip_change_log(text)
    if changed:
        if dry_run:
            log_lines.append(f"DRY RUN: would remove change_log_url from {md_file.relative_to(ROOT_DIR)}")
        else:
            md_file.write_text(new_text, encoding='utf-8')
            log_lines.append(f"UPDATED: removed change_log_url from {md_file.relative_to(ROOT_DIR)}")
    return changed


def main():
    parser = argparse.ArgumentParser(description='Remove change_log_url frontmatter key from standards markdown files')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')
    log_file = ROOT_DIR / 'tools' / 'reports' / f'changelog-metadata-removal-{timestamp}.log'
    log_lines = [
        f"Changelog Metadata Removal Log - {datetime.now(timezone.utc).isoformat()}",
        f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}",
        '=' * 60,
        ''
    ]

    md_files = list(STANDARDS_DIR.glob('**/*.md'))
    total = len(md_files)
    touched = 0
    for md in md_files:
        if process_file(md, args.dry_run, log_lines):
            touched += 1

    log_lines.extend([
        '', '=' * 60,
        f'Files scanned: {total}',
        f'Files modified: {touched}',
    ])

    # Write log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('\n'.join(log_lines), encoding='utf-8')
    print(f"Log written to: {log_file.relative_to(ROOT_DIR)}")
    print(f"Files modified: {touched} / {total}")

    if args.dry_run:
        return 0
    else:
        # Python-based verification to ensure cross-platform compatibility (no grep required)
        remaining_count = 0
        for md in STANDARDS_DIR.glob('**/*.md'):
            if 'change_log_url:' in md.read_text(encoding='utf-8'):
                remaining_count += 1
        if remaining_count == 0:
            print('Verification passed: No remaining change_log_url keys.')
            return 0
        else:
            print(f'Verification failed: {remaining_count} occurrences still present.')
            return 1


if __name__ == '__main__':
    sys.exit(main())