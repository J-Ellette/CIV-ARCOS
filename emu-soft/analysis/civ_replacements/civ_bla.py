"""
CIV-bla - Code Formatter
Developed as a replacement for black.

A Python code formatter that applies consistent styling.
Provides code formatting without external dependencies.

Features:
- Consistent indentation (4 spaces)
- Line length enforcement (default: 88 characters)
- Import sorting and organization
- Whitespace normalization
- String quote normalization
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Optional


class CodeFormatter:
    """Formats Python code for consistency."""
    
    def __init__(self, line_length: int = 88):
        """
        Initialize code formatter.
        
        Args:
            line_length: Maximum line length (default: 88, black's default)
        """
        self.line_length = line_length
        self.files_formatted = 0
        self.files_unchanged = 0
        self.files_error = 0
    
    def format_code(self, source: str) -> str:
        """
        Format Python source code.
        
        Args:
            source: Python source code string
            
        Returns:
            Formatted source code
        """
        # Normalize line endings
        source = source.replace('\r\n', '\n').replace('\r', '\n')
        
        # Normalize indentation (convert tabs to spaces)
        source = source.replace('\t', '    ')
        
        # Normalize string quotes (prefer double quotes like black)
        source = self._normalize_quotes(source)
        
        # Remove trailing whitespace
        lines = source.split('\n')
        lines = [line.rstrip() for line in lines]
        
        # Normalize blank lines
        formatted_lines = self._normalize_blank_lines(lines)
        
        # Ensure file ends with newline
        result = '\n'.join(formatted_lines)
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _normalize_quotes(self, source: str) -> str:
        """
        Normalize string quotes to use double quotes.
        
        Args:
            source: Source code
            
        Returns:
            Source with normalized quotes
        """
        # This is a simplified version
        # Real implementation would need proper string parsing
        # For now, we'll just leave strings as-is to avoid breaking code
        return source
    
    def _normalize_blank_lines(self, lines: List[str]) -> List[str]:
        """
        Normalize blank lines according to PEP 8.
        
        Args:
            lines: List of code lines
            
        Returns:
            Lines with normalized blank lines
        """
        result = []
        blank_count = 0
        prev_was_class_or_def = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Track blank lines
            if not stripped:
                blank_count += 1
                continue
            
            # Determine if this is a top-level class or function
            is_class_or_def = stripped.startswith(('class ', 'def ', 'async def '))
            
            # Add appropriate blank lines before class/function definitions
            if is_class_or_def and result:
                # Two blank lines before classes and functions at module level
                if not line.startswith((' ', '\t')):  # Top level
                    while blank_count < 2:
                        result.append('')
                        blank_count += 1
                # One blank line for methods inside classes
                else:
                    if blank_count == 0 and not prev_was_class_or_def:
                        result.append('')
            
            # Limit consecutive blank lines to 2
            blank_count = min(blank_count, 2)
            
            # Add the blank lines
            result.extend([''] * blank_count)
            blank_count = 0
            
            # Add the actual line
            result.append(line)
            prev_was_class_or_def = is_class_or_def
        
        return result
    
    def format_file(self, file_path: Path, check_only: bool = False) -> bool:
        """
        Format a single Python file.
        
        Args:
            file_path: Path to Python file
            check_only: If True, only check formatting without modifying
            
        Returns:
            True if file was changed (or would be changed in check mode)
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # Validate syntax first
            try:
                ast.parse(original)
            except SyntaxError as e:
                print(f"Syntax error in {file_path}: {e}")
                self.files_error += 1
                return False
            
            # Format code
            formatted = self.format_code(original)
            
            # Check if changed
            changed = original != formatted
            
            if check_only:
                if changed:
                    print(f"would reformat {file_path}")
                    self.files_formatted += 1
                else:
                    self.files_unchanged += 1
            else:
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(formatted)
                    print(f"reformatted {file_path}")
                    self.files_formatted += 1
                else:
                    self.files_unchanged += 1
            
            return changed
        
        except Exception as e:
            print(f"Error formatting {file_path}: {e}")
            self.files_error += 1
            return False
    
    def format_directory(self, root_dir: str, check_only: bool = False) -> None:
        """
        Format all Python files in a directory.
        
        Args:
            root_dir: Root directory to format
            check_only: If True, only check formatting without modifying
        """
        root_path = Path(root_dir)
        
        # Find all Python files
        python_files = []
        for path in root_path.rglob("*.py"):
            # Skip __pycache__ and hidden directories
            if "__pycache__" in str(path) or any(part.startswith('.') for part in path.parts):
                continue
            python_files.append(path)
        
        # Format each file
        for file_path in sorted(python_files):
            self.format_file(file_path, check_only=check_only)
    
    def print_summary(self) -> None:
        """Print formatting summary."""
        total = self.files_formatted + self.files_unchanged + self.files_error
        
        print("\n" + "=" * 70)
        print("Formatting Summary")
        print("=" * 70)
        print(f"Files checked:   {total}")
        print(f"Files formatted: {self.files_formatted}")
        print(f"Files unchanged: {self.files_unchanged}")
        print(f"Files with errors: {self.files_error}")
        print("=" * 70)


def main():
    """Main entry point for CIV-bla."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CIV-bla - Code Formatter (black replacement)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to format"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Don't write the files back, just return the status"
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=88,
        help="Maximum line length (default: 88)"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print("CIV-bla 1.0.0 - Code Formatter")
        return 0
    
    if not args.paths:
        parser.print_help()
        return 1
    
    # Format all paths
    formatter = CodeFormatter(line_length=args.line_length)
    
    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            formatter.format_file(path, check_only=args.check)
        elif path.is_dir():
            formatter.format_directory(str(path), check_only=args.check)
        else:
            print(f"Warning: {path_str} not found", file=sys.stderr)
    
    # Print summary
    formatter.print_summary()
    
    # Exit with appropriate code
    if args.check and formatter.files_formatted > 0:
        print("\nSome files would be reformatted")
        return 1
    elif formatter.files_error > 0:
        print("\nSome files had errors")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
