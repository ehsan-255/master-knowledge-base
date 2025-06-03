import os
import re
import glob

def update_changelog_references():
    """Update all change_log_url references to point to parent changelog files"""
    
    # Define the mapping of directories to their parent changelog files
    updates_made = 0
    files_processed = 0
    
    # Process all .md files in standards subdirectories
    standards_pattern = "master-knowledge-base/standards/**/*.md"
    for filepath in glob.glob(standards_pattern, recursive=True):
        if "changelog.md" in filepath.lower():
            continue  # Skip the changelog files themselves
            
        files_processed += 1
        
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it contains change_log_url
            if 'change_log_url:' not in content:
                continue
                
            # Determine the relative path to standards/changelog.md
            if "standards/src/" in filepath:
                relative_path = "../changelog.md"
            elif "standards/registry/" in filepath:
                relative_path = "../changelog.md"
            elif "standards/templates/" in filepath:
                relative_path = "../changelog.md"
            else:
                relative_path = "./changelog.md"  # For files directly in standards/
            
            # Update the change_log_url line - handle various patterns
            patterns = [
                r'change_log_url: \./[A-Z0-9-]+-CHANGELOG\.MD',  # Uppercase .MD
                r'change_log_url: \./[A-Z0-9-]+-changelog\.md',  # Lowercase .md
            ]
            
            new_content = content
            for pattern in patterns:
                new_content = re.sub(pattern, f'change_log_url: {relative_path}', new_content)
                
            # Also fix any files that might have the wrong relative path due to my earlier script bug
            if "standards/src/" in filepath or "standards/registry/" in filepath or "standards/templates/" in filepath:
                # Files in subdirectories should use ../changelog.md, not ./changelog.md
                new_content = re.sub(r'change_log_url: \./changelog\.md', f'change_log_url: {relative_path}', new_content)
            
            # Check if any changes were made
            if new_content != content:
                # Write back the updated content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updates_made += 1
                print(f"Updated: {filepath}")
                
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    # Process tools files to point to tools/changelog.md
    tools_pattern = "master-knowledge-base/tools/**/*.md"
    for filepath in glob.glob(tools_pattern, recursive=True):
        if "changelog.md" in filepath.lower():
            continue  # Skip the changelog files themselves
            
        files_processed += 1
        
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it contains change_log_url
            if 'change_log_url:' not in content:
                continue
                
            # Update placeholder URLs to point to tools changelog
            patterns_to_replace = [
                r'change_log_url: "https://example\.com/placeholder-changelog-url"',
                r'change_log_url: https://example\.com/placeholder-changelog-url'
            ]
            
            for pattern in patterns_to_replace:
                new_content = re.sub(pattern, 'change_log_url: ./changelog.md', content)
                if new_content != content:
                    content = new_content
                    # Write back the updated content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updates_made += 1
                    print(f"Updated tools file: {filepath}")
                    break
                
        except Exception as e:
            print(f"Error processing tools file {filepath}: {e}")
    
    print(f"\nSummary:")
    print(f"Files processed: {files_processed}")
    print(f"Updates made: {updates_made}")

if __name__ == "__main__":
    update_changelog_references() 