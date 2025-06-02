import yaml
import re
from datetime import datetime, timezone
import sys # For reading command-line arguments

# --- Helper function to parse frontmatter and body ---
def parse_markdown_file_content(content):
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    frontmatter_str = parts[1]
    body_str = parts[2]
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        if frontmatter is None:
            frontmatter = {}
        return frontmatter, body_str
    except yaml.YAMLError:
        return {}, content

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def increment_version(version_str):
    if not version_str:
        return "1.0.0"

    version_str = str(version_str)

    match = re.match(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(.*)", version_str)
    if not match:
        return "1.0.0"

    major, minor, patch, suffix = match.groups()

    major = int(major)
    minor = int(minor) if minor is not None else 0
    patch = int(patch) if patch is not None else 0

    minor += 1
    patch = 0

    return f"{major}.{minor}.{patch}{suffix if suffix else ''}"

deprecation_notice_template = """
**DEPRECATED:** This collection document is superseded by the new atomic standards architecture. Relevant content has been refactored into individual standard, policy, and guide documents located in `/master-knowledge-base/standards/src/`. Please refer to `[[AS-ROOT-STANDARDS-KB]]` for an overview of the new standards or consult `[[GM-GUIDE-KB-USAGE]]`.
"""

current_utc_time_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
processed_files_for_tool = []

# Read filepaths from command line arguments
target_filepaths = sys.argv[1:]

if not target_filepaths:
    print("Usage: python deprecate_collections.py <file1.md> <file2.md> ...")
    sys.exit(1)

for filepath in target_filepaths:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"--- ERROR: File not found {filepath} ---")
        continue
    except Exception as e:
        print(f"--- ERROR: Could not read file {filepath}: {e} ---")
        continue

    frontmatter, body = parse_markdown_file_content(content)

    if 'tags' not in frontmatter or not isinstance(frontmatter['tags'], list):
        frontmatter['tags'] = []

    current_tags = frontmatter.get('tags', [])
    new_tags = [tag for tag in current_tags if not tag.startswith("status/")]
    new_tags.append("status/deprecated")
    frontmatter['tags'] = sorted(list(set(new_tags)))

    frontmatter['date-modified'] = current_utc_time_str

    current_version = frontmatter.get('version', '0.0.0')
    frontmatter['version'] = increment_version(current_version)

    body_lines = body.lstrip().split('\n')
    new_body = ""
    notice_already_present = False

    # Check if the new deprecation notice is already at the top of the body
    if body.lstrip().startswith(deprecation_notice_template.strip()):
        notice_already_present = True
        new_body = body # Keep body as is

    if not notice_already_present:
        cleaned_body_lines = []
        # Try to remove any older <font color="red"> deprecation notice
        old_notice_signature_line = "<font color=\"red\">IMPORTANT: This document is deprecated.</font>"
        old_notice_end_signature = "[[GM-GUIDE-KB-USAGE_ID_PLACEHOLDER]]" # Heuristic end marker

        idx = 0
        while idx < len(body_lines):
            line_stripped = body_lines[idx].strip()
            if line_stripped.startswith(old_notice_signature_line):
                # Found the start of an old notice, now try to find its end
                block_to_skip_end_idx = idx
                for j_idx in range(idx, min(idx + 15, len(body_lines))): # Search a few lines down
                    if old_notice_end_signature in body_lines[j_idx]:
                        block_to_skip_end_idx = j_idx
                        break
                else: # if end signature not found, assume old notice is just the starting line
                    block_to_skip_end_idx = idx

                idx = block_to_skip_end_idx + 1

                # Skip potential "---" separator after the old notice
                if idx < len(body_lines) and body_lines[idx].strip() == "---":
                    idx += 1
                # Skip any blank lines immediately following
                while idx < len(body_lines) and not body_lines[idx].strip():
                    idx += 1
                continue # Continue to process lines after the skipped block

            cleaned_body_lines.append(body_lines[idx])
            idx += 1

        body_content_for_notice = "\n".join(cleaned_body_lines)

        # Add new notice
        if body_content_for_notice.lstrip().startswith("# "): # H1 heading
            temp_lines = body_content_for_notice.lstrip().split('\n')
            insert_point = 1 # After H1
            while insert_point < len(temp_lines) and not temp_lines[insert_point].strip(): # Skip blank lines after H1
                insert_point += 1
            new_body = "\n".join(temp_lines[:insert_point]) + "\n\n" + deprecation_notice_template.strip() + "\n\n" + "\n".join(temp_lines[insert_point:]).lstrip()
        else:
            new_body = deprecation_notice_template.strip() + "\n\n" + body_content_for_notice.lstrip()

    if 'title' not in frontmatter: frontmatter['title'] = f"DEPRECATED COLLECTION - {filepath.split('/')[-1]}"
    if 'aliases' not in frontmatter: frontmatter['aliases'] = [filepath.split('/')[-1].replace('.md','')]

    new_frontmatter_yaml = yaml.dump(frontmatter, sort_keys=False, Dumper=NoAliasDumper, width=1000, allow_unicode=True)
    updated_content = f"---\n{new_frontmatter_yaml}---\n{new_body.strip()}" # Ensure body is stripped at the end

    processed_files_for_tool.append({"filename": filepath, "content": updated_content})

for item in processed_files_for_tool:
    print(f"--- START OF {item['filename']} ---")
    print(item['content'])
    print(f"--- END OF {item['filename']} ---\n")

print("Script deprecate_collections.py finished processing specified files.")
