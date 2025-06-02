import sys
import json
import yaml
import re

def extract_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f: # Corrected typo
            content = f.read()
    except FileNotFoundError:
        return {"filepath": filepath, "error": "File not found"}
    except Exception as e:
        return {"filepath": filepath, "error": f"Error reading file: {str(e)}"}

    data = {"filepath": filepath}
    try:
        fm_match = re.match(r'^---\s*\n(.*?\n)^---\s*\n', content, re.DOTALL | re.MULTILINE)
        if fm_match:
            frontmatter_str = fm_match.group(1)
            fm = yaml.safe_load(frontmatter_str)
            if fm is None:
                fm = {}

            data['standard_id'] = fm.get('standard_id', fm.get('id'))
            data['title'] = fm.get('title')
            data['info-type'] = fm.get('info-type')
            related = fm.get('related-standards')
            if isinstance(related, str):
                data['related-standards'] = [related] if related.upper() != "N/A" else []
            elif isinstance(related, list):
                data['related-standards'] = related
            else:
                data['related-standards'] = [] # Ensure it's always a list

        else:
            data['error'] = "No frontmatter found"

    except yaml.YAMLError as e:
        data['error'] = f"YAML parsing error: {str(e)}"
    except Exception as e:
        data['error'] = f"General error parsing frontmatter: {str(e)}"

    return data

if __name__ == '__main__':
    filepaths_str = sys.argv[1]
    filepaths = json.loads(filepaths_str)
    results = []
    for fp in filepaths:
        results.append(extract_data(fp))

    print(json.dumps(results, indent=2))
