#!/usr/bin/env python3
"""
TODO Tracking Script for Knowledge Base

Scans for > [!TODO] markers in markdown files and generates reports.
Compatible with Obsidian callout syntax.
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class TodoItem:
    file_path: str
    line_number: int
    content: str
    context_before: List[str]
    context_after: List[str]
    created_date: str

class TodoTracker:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.todo_pattern = re.compile(r'^>\s*\[!TODO\](.*)$', re.MULTILINE | re.IGNORECASE)
        self.todos: List[TodoItem] = []
    
    def extract_context(self, lines: List[str], todo_line_idx: int, context_lines: int = 2) -> tuple:
        """Extract context lines before and after TODO"""
        start_idx = max(0, todo_line_idx - context_lines)
        end_idx = min(len(lines), todo_line_idx + context_lines + 1)
        
        context_before = lines[start_idx:todo_line_idx]
        context_after = lines[todo_line_idx + 1:end_idx]
        
        return context_before, context_after
    
    def scan_file(self, file_path: Path) -> List[TodoItem]:
        """Scan a single file for TODO items"""
        todos = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Find all TODO matches
            for match in self.todo_pattern.finditer(content):
                # Find line number
                line_start = content[:match.start()].count('\n')
                todo_content = match.group(1).strip()
                
                # Get context
                context_before, context_after = self.extract_context(lines, line_start)
                
                todo = TodoItem(
                    file_path=str(file_path.relative_to(self.root_dir)),
                    line_number=line_start + 1,  # 1-indexed
                    content=todo_content,
                    context_before=context_before,
                    context_after=context_after,
                    created_date=datetime.now().strftime('%Y-%m-%d')
                )
                
                todos.append(todo)
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return todos
    
    def scan_directory(self, directory: Path = None, exclude_patterns: List[str] = None) -> int:
        """Scan directory for TODO items"""
        if directory is None:
            directory = self.root_dir
        
        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', 'node_modules', '.vscode']
        
        self.todos = []
        scanned_count = 0
        
        for md_file in directory.rglob("*.md"):
            # Check if file should be excluded
            if any(pattern in str(md_file) for pattern in exclude_patterns):
                continue
            
            file_todos = self.scan_file(md_file)
            self.todos.extend(file_todos)
            scanned_count += 1
        
        return scanned_count
    
    def save_todos_json(self, output_file: Path):
        """Save TODOs to JSON file"""
        data = {
            "scan_date": datetime.now().isoformat(),
            "root_directory": str(self.root_dir),
            "total_todos": len(self.todos),
            "todos": [asdict(todo) for todo in self.todos]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def generate_markdown_report(self, output_file: Path):
        """Generate markdown report of TODOs"""
        report_lines = [
            "# TODO Report",
            f"",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Root Directory**: `{self.root_dir}`",
            f"**Total TODOs**: {len(self.todos)}",
            f"",
            "## Summary by File",
            ""
        ]
        
        # Group by file
        by_file: Dict[str, List[TodoItem]] = {}
        for todo in self.todos:
            if todo.file_path not in by_file:
                by_file[todo.file_path] = []
            by_file[todo.file_path].append(todo)
        
        # Summary table
        report_lines.extend([
            "| File | TODOs |",
            "|------|-------|"
        ])
        
        for file_path, todos in sorted(by_file.items()):
            report_lines.append(f"| `{file_path}` | {len(todos)} |")
        
        report_lines.extend(["", "## Detailed TODOs", ""])
        
        # Detailed listings
        for file_path, todos in sorted(by_file.items()):
            report_lines.extend([
                f"### `{file_path}`",
                ""
            ])
            
            for todo in sorted(todos, key=lambda t: t.line_number):
                report_lines.extend([
                    f"**Line {todo.line_number}**: {todo.content}",
                    ""
                ])
                
                if todo.context_before:
                    report_lines.append("*Context before:*")
                    for line in todo.context_before[-2:]:  # Last 2 lines
                        report_lines.append(f"```")
                        report_lines.append(line)
                        report_lines.append(f"```")
                    report_lines.append("")
                
                if todo.context_after:
                    report_lines.append("*Context after:*")
                    for line in todo.context_after[:2]:  # First 2 lines
                        report_lines.append(f"```")
                        report_lines.append(line)
                        report_lines.append(f"```")
                    report_lines.append("")
                
                report_lines.append("---")
                report_lines.append("")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
    
    def generate_console_report(self):
        """Print TODO summary to console"""
        print(f"\n[TODO REPORT]")
        print(f"{'='*50}")
        print(f"Root Directory: {self.root_dir}")
        print(f"Total TODOs: {len(self.todos)}")
        print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.todos:
            print("\n[✓] No TODOs found!")
            return
        
        # Group by file
        by_file: Dict[str, List[TodoItem]] = {}
        for todo in self.todos:
            if todo.file_path not in by_file:
                by_file[todo.file_path] = []
            by_file[todo.file_path].append(todo)
        
        print(f"\n[Files] Files with TODOs:")
        for file_path, todos in sorted(by_file.items()):
            print(f"  {file_path}: {len(todos)} TODOs")
        
        print(f"\n[Items] Recent TODOs (first 5):")
        for i, todo in enumerate(self.todos[:5]):
            print(f"  {i+1}. {todo.file_path}:{todo.line_number}")
            print(f"     {todo.content[:80]}{'...' if len(todo.content) > 80 else ''}")
        
        if len(self.todos) > 5:
            print(f"     ... and {len(self.todos) - 5} more")
    
    def get_stats(self) -> Dict:
        """Get TODO statistics"""
        by_file = {}
        for todo in self.todos:
            if todo.file_path not in by_file:
                by_file[todo.file_path] = 0
            by_file[todo.file_path] += 1
        
        return {
            "total_todos": len(self.todos),
            "files_with_todos": len(by_file),
            "avg_todos_per_file": len(self.todos) / len(by_file) if by_file else 0,
            "files_breakdown": by_file
        }

def main():
    parser = argparse.ArgumentParser(description="Track TODO items in markdown files")
    parser.add_argument("--root", "-r", default=".", help="Root directory to scan")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for TODOs and save to JSON")
    scan_parser.add_argument("--output", "-o", default="todos.json", help="Output JSON file")
    scan_parser.add_argument("--directory", "-d", help="Directory to scan (default: root)")
    scan_parser.add_argument("--exclude", nargs="*", default=[".git", "__pycache__", "node_modules"], 
                           help="Patterns to exclude")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate TODO report")
    report_parser.add_argument("--format", "-f", choices=["markdown", "console", "json"], 
                             default="console", help="Output format")
    report_parser.add_argument("--output", "-o", help="Output file (for markdown/json)")
    report_parser.add_argument("--input", "-i", help="Input JSON file (instead of scanning)")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show TODO statistics")
    stats_parser.add_argument("--input", "-i", help="Input JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tracker = TodoTracker(args.root)
    
    if args.command == "scan":
        scan_dir = Path(args.directory) if args.directory else tracker.root_dir
        count = tracker.scan_directory(scan_dir, args.exclude)
        print(f"Scanned {count} files, found {len(tracker.todos)} TODOs")
        
        tracker.save_todos_json(Path(args.output))
        print(f"Saved TODOs to {args.output}")
        
        # Also show console summary
        tracker.generate_console_report()
    
    elif args.command == "report":
        if args.input:
            # Load from JSON
            with open(args.input, 'r') as f:
                data = json.load(f)
                tracker.todos = [TodoItem(**todo) for todo in data["todos"]]
        else:
            # Scan first
            tracker.scan_directory()
        
        if args.format == "console":
            tracker.generate_console_report()
        elif args.format == "markdown":
            output_file = Path(args.output) if args.output else Path("todo-report.md")
            tracker.generate_markdown_report(output_file)
            print(f"Generated markdown report: {output_file}")
        elif args.format == "json":
            output_file = Path(args.output) if args.output else Path("todos.json")
            tracker.save_todos_json(output_file)
            print(f"Generated JSON report: {output_file}")
    
    elif args.command == "stats":
        if args.input:
            with open(args.input, 'r') as f:
                data = json.load(f)
                tracker.todos = [TodoItem(**todo) for todo in data["todos"]]
        else:
            tracker.scan_directory()
        
        stats = tracker.get_stats()
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main() 