#!/usr/bin/env python3
"""
Repository Tree Generator

Generates a formatted repository tree structure using configuration files:
- .treeignore: Folders to completely exclude
- .subtreeignore: Folders to show but not expand contents
- .treeaddtext: Annotations for specific paths
- .treeicon: Icons for specific paths

Usage: python main_repo_tree.py
Output: repo-tree.md in root directory
"""

import os
import fnmatch
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class RepositoryTreeGenerator:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.output_file = self.root_path / "repo-tree.md"
        
        # Configuration files are now in repo-tree folder
        # If we're already in the repo-tree folder, use current directory
        current_dir = Path.cwd()
        if current_dir.name == 'repo-tree':
            self.config_path = current_dir
        else:
            self.config_path = self.root_path / "master-knowledge-base" / "tools" / "utilities" / "repo-tree"

        
        # Load configuration from files
        self.ignore_patterns = self._load_ignore_patterns()
        self.subtree_ignore_paths = self._load_subtree_ignore_paths()
        self.folder_annotations = self._load_folder_annotations()
        self.folder_icons, self.icon_descriptions_from_treeicon = self._load_folder_icons()
        
        # File extensions to include
        self.included_extensions = {
            '.md', '.py', '.yaml', '.yml', '.json', '.txt', '.js', '.ts',
            '.html', '.css', '.sh', '.bat', '.ps1', '.xml', '.toml'
        }

    def _load_ignore_patterns(self) -> List[str]:
        """Load ignore patterns from .treeignore file."""
        ignore_file = self.config_path / ".treeignore"
        patterns = []
        
        if ignore_file.exists():
            try:
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except Exception as e:
                print(f"Warning: Could not read .treeignore: {e}")
        
        return patterns

    def _load_subtree_ignore_paths(self) -> Set[str]:
        """Load paths that should be shown but not expanded from .subtreeignore."""
        ignore_file = self.config_path / ".subtreeignore"
        paths = set()
        
        if ignore_file.exists():
            try:
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            paths.add(line)
            except Exception as e:
                print(f"Warning: Could not read .subtreeignore: {e}")
        
        return paths

    def _load_folder_annotations(self) -> Dict[str, str]:
        """Load folder annotations from .treeaddtext file."""
        annotations_file = self.config_path / ".treeaddtext"
        annotations = {}
        
        if annotations_file.exists():
            try:
                with open(annotations_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#') and '|' in line:
                            path, annotation = line.split('|', 1)
                            annotations[path.strip()] = annotation.strip()
            except Exception as e:
                print(f"Warning: Could not read .treeaddtext: {e}")
        
        return annotations

    def _load_folder_icons(self):
        """Load folder icons and descriptions from .treeicon file.
        
        Returns:
            tuple: (icons_dict, descriptions_dict)
        """
        icons_file = self.config_path / ".treeicon"
        icons = {}
        descriptions = {}
        
        if icons_file.exists():
            try:
                with open(icons_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#') and '|' in line:
                            parts = line.split('|')
                            if len(parts) >= 2:
                                path = parts[0].strip()
                                icon = parts[1].strip()
                                icons[path] = icon
                                
                                # If description provided, store it
                                if len(parts) >= 3:
                                    description = parts[2].strip()
                                    descriptions[icon] = description

            except Exception as e:
                print(f"Warning: Could not read .treeicon: {e}")

        
        return icons, descriptions

    def _generate_legend(self) -> str:
        """Generate legend dynamically from the icon configuration."""
        legend_items = []
        
        # Combine descriptions from .treeicon with fallback defaults
        default_descriptions = {
            '📁': 'Standard Directory',
            '📄': 'File',
            '⛔': 'System/Ignored Directory', 
            '✅': 'Important Directory (with specific requirements)',
            '❌': 'Restricted Directory (with usage restrictions)',
            '🔧': 'Tools/Build Directory',
            '📋': 'Documentation/Standards Directory',
            '🎯': 'Project Management Directory',
            '📇': 'Indexing Directory',
            '🔍': 'Linting/Validation Directory',
            '🔄': 'Refactoring Directory',
            '🏗️': 'Building Directory',
            '📊': 'Registry/Data Directory',
            '📝': 'Source/Content Directory',
            '📚': 'Documentation Directory',
            '💡': 'Examples/Samples Directory',
            '💾': 'Backup Directory',
            '🗂️': 'Temporary Directory'
        }
        
        # Merge descriptions: .treeicon descriptions override defaults
        icon_descriptions = {**default_descriptions, **self.icon_descriptions_from_treeicon}
        
        # Collect unique icons from configuration
        used_icons = set()
        for icon in self.folder_icons.values():
            used_icons.add(icon)
        
        # Add default icons that are always used
        used_icons.update(['📁', '📄'])
        

        
        # Build legend with descriptions or placeholders
        for icon in sorted(used_icons):
            if icon in icon_descriptions:
                legend_items.append(f"- {icon} **{icon_descriptions[icon]}**")
            else:
                legend_items.append(f"- {icon} **[Icon Description Not Set]**")
        
        return "\n".join(legend_items)

    def should_ignore_completely(self, path: Path) -> bool:
        """Check if a path should be completely ignored based on .treeignore patterns."""
        path_name = path.name
        relative_path = self.get_relative_path(path)
        
        for pattern in self.ignore_patterns:
            # Check against folder name
            if fnmatch.fnmatch(path_name, pattern):
                return True
            # Check against relative path
            if fnmatch.fnmatch(relative_path, pattern):
                return True
            # Check against absolute pattern
            if pattern in relative_path:
                return True
        
        return False

    def should_ignore_subtree(self, path: Path) -> bool:
        """Check if a path should be shown but contents ignored."""
        relative_path = self.get_relative_path(path)
        return relative_path in self.subtree_ignore_paths

    def get_folder_icon(self, folder_path: Path, relative_path: str) -> str:
        """Get appropriate icon for folder based on configuration."""
        folder_name = folder_path.name
        
        # Check for specific relative paths first
        if relative_path in self.folder_icons:
            return self.folder_icons[relative_path]
            
        # Check for folder name patterns
        if folder_name in self.folder_icons:
            return self.folder_icons[folder_name]
            
        # Default folder icon
        return '📁'

    def get_folder_annotation(self, folder_path: Path, relative_path: str) -> str:
        """Get annotation text for folders based on configuration."""
        folder_name = folder_path.name
        
        # Check for specific relative paths first
        if relative_path in self.folder_annotations:
            return f" {self.folder_annotations[relative_path]}"
            
        # Check for folder name patterns
        if folder_name in self.folder_annotations:
            return f" {self.folder_annotations[folder_name]}"
        
        return ""

    def should_include_file(self, file_path: Path) -> bool:
        """Determine if a file should be included in the tree."""
        # Check if file is ignored
        if self.should_ignore_completely(file_path):
            return False
            
        # Include files with specific extensions
        if file_path.suffix.lower() in self.included_extensions:
            return True
            
        # Include files without extensions (like .gitignore, .cursorignore)
        if file_path.suffix == '' and file_path.name.startswith('.'):
            return True
            
        return False

    def get_relative_path(self, path: Path) -> str:
        """Get relative path from root, handling master-knowledge-base properly."""
        try:
            rel_path = path.relative_to(self.root_path)
            return str(rel_path).replace('\\', '/')
        except ValueError:
            return str(path).replace('\\', '/')

    def generate_tree_recursive(self, current_path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """Recursively generate tree structure."""
        lines = []
        
        # Check if path should be completely ignored
        if self.should_ignore_completely(current_path):
            return lines
        
        relative_path = self.get_relative_path(current_path)
        
        # Skip the root directory itself
        if current_path != self.root_path:
            icon = self.get_folder_icon(current_path, relative_path)
            annotation = self.get_folder_annotation(current_path, relative_path)
            
            lines.append(f"{prefix}{icon} {current_path.name}{annotation}")
            
            # Check if we should ignore the subtree (show folder but not contents)
            if self.should_ignore_subtree(current_path):
                return lines
            
            # Update prefix for children
            new_prefix = prefix + ("    " if is_last else "│   ")
        else:
            new_prefix = ""
        
        # Get children (directories and files)
        try:
            children = []
            
            # Add directories first
            dirs = []
            for d in current_path.iterdir():
                if d.is_dir() and not self.should_ignore_completely(d):
                    dirs.append(d)
            dirs.sort()
            
            # Add files
            files = []
            for f in current_path.iterdir():
                if f.is_file() and self.should_include_file(f):
                    files.append(f)
            files.sort()
            
            children = dirs + files
            
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                child_prefix = new_prefix
                
                if child.is_dir():
                    # Recursively process directory
                    child_lines = self.generate_tree_recursive(child, child_prefix, is_last_child)
                    lines.extend(child_lines)
                else:
                    # Add file
                    lines.append(f"{child_prefix}📄 {child.name}")
        
        except PermissionError:
            # Skip directories we can't access
            pass
        
        return lines

    def generate_tree(self) -> str:
        """Generate the complete repository tree."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Start with root directory
        lines = [
            "```",
            "📁 master-knowledge-base"
        ]
        
        # Generate tree starting from root, but show master-knowledge-base as root
        tree_lines = self.generate_tree_recursive(self.root_path, "    ")
        lines.extend(tree_lines)
        
        lines.append("```")
        
        # Generate legend and configuration sections
        legend_section = f"""## Legend

{self._generate_legend()}"""

        config_section = f"""## Configuration Files

- **`.treeignore`**: Folders to completely exclude from tree
- **`.subtreeignore`**: Folders to show but not expand contents  
- **`.treeaddtext`**: Annotations for specific folders/files
- **`.treeicon`**: Icons and legend descriptions (format: `path|icon|description`)

**Configuration Location**: `master-knowledge-base/tools/utilities/repo-tree/`"""

        header = f"""# Repository Tree Structure

**Generated**: {timestamp}  
**Script**: `master-knowledge-base/tools/utilities/repo-tree/main_repo_tree.py`  
**Output**: Automated repository structure overview  

---

## Repository Structure

"""
        
        # Combine everything with legend and config at the bottom
        content = header + "\n".join(lines) + f"\n\n---\n\n{legend_section}\n\n---\n\n{config_section}\n"
        
        return content

    def write_tree(self):
        """Generate and write the repository tree to file."""
        tree_content = self.generate_tree()
        
        try:
            with open(self.output_file, 'w', encoding='utf-8', errors='replace') as f:
                f.write(tree_content)
            
            try:
                print(f"✅ Repository tree generated successfully!")
                print(f"📄 Output file: {self.output_file}")
                print(f"📊 Total lines: {len(tree_content.splitlines())}")
            except UnicodeEncodeError:
                print(f"Repository tree generated successfully!")
                print(f"Output file: {self.output_file}")
                print(f"Total lines: {len(tree_content.splitlines())}")
            
        except Exception as e:
            try:
                print(f"❌ Error writing tree file: {e}")
            except UnicodeEncodeError:
                print(f"Error writing tree file: {e}")
            return False
        
        return True

def main():
    """Main function to generate repository tree."""
    try:
        print("🎯 Generating Repository Tree Structure...")
    except UnicodeEncodeError:
        print("Generating Repository Tree Structure...")
    print("-" * 50)
    
    # Find the repository root (look for master-knowledge-base directory)
    current_dir = Path.cwd()
    repo_root = current_dir
    
    # If we're inside master-knowledge-base, go up to find the actual root
    if current_dir.name == 'master-knowledge-base':
        repo_root = current_dir
    elif (current_dir / 'master-knowledge-base').exists():
        repo_root = current_dir
    else:
        # Look for master-knowledge-base in parent directories
        for parent in current_dir.parents:
            if parent.name == 'master-knowledge-base':
                repo_root = parent
                break
            elif (parent / 'master-knowledge-base').exists():
                repo_root = parent
                break
    
    try:
        print(f"📁 Repository root: {repo_root}")
    except UnicodeEncodeError:
        print(f"Repository root: {repo_root}")
    
    generator = RepositoryTreeGenerator(repo_root)
    success = generator.write_tree()
    
    if success:
        try:
            print("\n🚀 Repository tree generation completed!")
            print(f"📍 Tree saved to: repo-tree.md")
        except UnicodeEncodeError:
            print("\nRepository tree generation completed!")
            print(f"Tree saved to: repo-tree.md")
    else:
        try:
            print("\n❌ Repository tree generation failed!")
        except UnicodeEncodeError:
            print("\nRepository tree generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 