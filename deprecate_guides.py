import yaml
import re
from datetime import datetime, timezone
import sys

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

current_utc_time_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
processed_files_for_tool = []

args = sys.argv[1:]
if not args or len(args) % 2 != 0:
    print("Usage: python deprecate_guides.py <file1.md> <replacement_info1> <file2.md> <replacement_info2> ...")
    sys.exit(1)

target_files_data = []
for i in range(0, len(args), 2):
    target_files_data.append({"path": args[i], "replacement_info": args[i+1]})

for file_data in target_files_data:
    filepath = file_data["path"]
    replacement_info = file_data["replacement_info"]

    if replacement_info.startswith("[[") and replacement_info.endswith("]]"):
        deprecation_notice = f"**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: {replacement_info}."
    else:
        # Use the replacement_info directly as the reason text
        deprecation_notice = f"**DEPRECATED:** This document is superseded. {replacement_info}."

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"--- ERROR: File not found {filepath} ---")
        processed_files_for_tool.append({
            "filename": filepath,
            "content": f"ERROR: File not found {filepath}",
            "error": True
        })
        continue
    except Exception as e:
        print(f"--- ERROR: Could not read file {filepath}: {e} ---")
        processed_files_for_tool.append({
            "filename": filepath,
            "content": f"ERROR: Could not read file {filepath}: {e}",
            "error": True
        })
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

    if 'title' not in frontmatter:
        frontmatter['title'] = f"DEPRECATED - {filepath.split('/')[-1].replace('.md','')}"
    if 'aliases' not in frontmatter and not filepath.split('/')[-1].startswith("_"):
         frontmatter['aliases'] = [filepath.split('/')[-1].replace('.md','')]


    new_body = deprecation_notice + "\n\n" + body.lstrip()

    new_frontmatter_yaml = yaml.dump(frontmatter, sort_keys=False, Dumper=NoAliasDumper, width=1000, allow_unicode=True)
    updated_content = f"---\n{new_frontmatter_yaml}---\n{new_body.strip()}"

    processed_files_for_tool.append({"filename": filepath, "content": updated_content, "error": False})

for item in processed_files_for_tool:
    print(f"--- START OF {item['filename']} ---")
    print(item['content'])
    print(f"--- END OF {item['filename']} ---\n")

print("Script deprecate_guides.py finished processing specified files.")
