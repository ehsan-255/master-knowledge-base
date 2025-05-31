import os
import argparse

def convert_line_endings_in_file(filepath, dry_run=True):
    try:
        with open(filepath, 'rb') as f: # Read as binary to detect \r\n accurately
            content_bytes = f.read()
        
        # Detect if conversion is needed
        if b'\r\n' in content_bytes or (b'\r' in content_bytes and b'\n' not in content_bytes.replace(b'\r\n', b'')):
            print(f"INFO: CRLF/CR detected in {filepath}")
            if not dry_run:
                # Convert CRLF -> LF and CR -> LF
                content_bytes = content_bytes.replace(b'\r\n', b'\n')
                content_bytes = content_bytes.replace(b'\r', b'\n')
                try:
                    with open(filepath, 'wb') as f_write: # Write as binary
                        f_write.write(content_bytes)
                    print(f"  SUCCESS: Converted line endings in {filepath} to LF.")
                    return True # Changed
                except Exception as e_write:
                    print(f"  ERROR: Could not write updated file {filepath}: {e_write}")
                    return False # Not changed due to error
            else:
                print(f"  DRY RUN: Would convert line endings in {filepath} to LF.")
                return True # Would change
        # else:
            # print(f"  INFO: File {filepath} already has LF line endings.") # Can be too verbose
            
    except Exception as e:
        print(f"  ERROR: Could not process file {filepath}: {e}")
    return False # No change or error

def main():
    parser = argparse.ArgumentParser(description="Convert line endings of .md files from CRLF/CR to LF.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan recursively.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    args = parser.parse_args()

    print(f"Starting line ending conversion. Dry run: {args.dry_run}")
    
    files_would_change_count = 0
    files_actually_changed_count = 0
    total_files_scanned = 0

    for target_dir in args.target_dirs:
        abs_target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(abs_target_dir):
            print(f"ERROR: Target directory {abs_target_dir} not found. Skipping.")
            continue
        print(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.endswith(".md"):
                    total_files_scanned += 1
                    filepath = os.path.join(root, filename)
                    if convert_line_endings_in_file(filepath, dry_run=args.dry_run):
                        files_would_change_count +=1
                        if not args.dry_run:
                            files_actually_changed_count +=1
            
    print(f"Line ending conversion finished. Scanned {total_files_scanned} .md files.")
    if args.dry_run:
        print(f"  Files that would have line endings converted: {files_would_change_count}")
    else:
        print(f"  Files with line endings actually converted: {files_actually_changed_count}")

if __name__ == "__main__":
    main() 