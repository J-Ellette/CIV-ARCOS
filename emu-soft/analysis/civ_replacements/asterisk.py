"""Asterisk - AST parser

Abstract Syntax Tree parser for development tasks.
Wrapper around Python's ast module for static code analysis.
"""

import ast
from typing import Any, Dict, List, Optional, Union


class AsteriskVisitor(ast.NodeVisitor):
    """Base visitor for AST traversal"""
    
    def __init__(self):
        self.nodes = []
    
    def visit(self, node):
        """Visit a node and track it"""
        self.nodes.append(node)
        return super().visit(node)


class Asterisk:
    """
    Asterisk: AST parser
    
    Provides utilities for Abstract Syntax Tree parsing and analysis.
    """
    
    def __init__(self):
        """Initialize Asterisk"""
        self.parse_count = 0
        self.analysis_count = 0
    
    def parse(self, 
              source: str, 
              filename: str = '<string>',
              mode: str = 'exec') -> ast.AST:
        """
        Parse Python source code into AST.
        
        Args:
            source: Python source code
            filename: Filename for error messages
            mode: Parse mode ('exec', 'eval', 'single')
            
        Returns:
            AST node
        """
        tree = ast.parse(source, filename=filename, mode=mode)
        self.parse_count += 1
        return tree
    
    def parse_file(self, filepath: str) -> ast.AST:
        """
        Parse Python file into AST.
        
        Args:
            filepath: Path to Python file
            
        Returns:
            AST node
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.parse(source, filename=filepath)
    
    def dump(self, 
             node: ast.AST, 
             annotate_fields: bool = True,
             include_attributes: bool = False,
             indent: Optional[int] = None) -> str:
        """
        Dump AST as string.
        
        Args:
            node: AST node
            annotate_fields: Include field names
            include_attributes: Include attributes
            indent: Indentation level
            
        Returns:
            String representation of AST
        """
        return ast.dump(
            node, 
            annotate_fields=annotate_fields,
            include_attributes=include_attributes,
            indent=indent
        )
    
    def unparse(self, node: ast.AST) -> str:
        """
        Convert AST back to source code.
        
        Args:
            node: AST node
            
        Returns:
            Python source code
        """
        return ast.unparse(node)
    
    def literal_eval(self, source: str) -> Any:
        """
        Safely evaluate literal expressions.
        
        Args:
            source: Python literal expression
            
        Returns:
            Evaluated value
        """
        return ast.literal_eval(source)
    
    def walk(self, node: ast.AST) -> List[ast.AST]:
        """
        Walk all nodes in AST.
        
        Args:
            node: Root AST node
            
        Returns:
            List of all nodes
        """
        return list(ast.walk(node))
    
    def get_functions(self, source: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from source code.
        
        Args:
            source: Python source code
            
        Returns:
            List of function information
        """
        tree = self.parse(source)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'lineno': node.lineno,
                    'is_async': False
                }
                functions.append(func_info)
            elif isinstance(node, ast.AsyncFunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'lineno': node.lineno,
                    'is_async': True
                }
                functions.append(func_info)
        
        self.analysis_count += 1
        return functions
    
    def get_classes(self, source: str) -> List[Dict[str, Any]]:
        """
        Extract class definitions from source code.
        
        Args:
            source: Python source code
            
        Returns:
            List of class information
        """
        tree = self.parse(source)
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'bases': [self.unparse(base) for base in node.bases],
                    'lineno': node.lineno,
                    'methods': []
                }
                
                # Get methods
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        class_info['methods'].append(item.name)
                
                classes.append(class_info)
        
        self.analysis_count += 1
        return classes
    
    def get_imports(self, source: str) -> List[Dict[str, Any]]:
        """
        Extract import statements from source code.
        
        Args:
            source: Python source code
            
        Returns:
            List of import information
        """
        tree = self.parse(source)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'lineno': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'type': 'from',
                        'module': node.module or '',
                        'name': alias.name,
                        'alias': alias.asname,
                        'lineno': node.lineno
                    })
        
        self.analysis_count += 1
        return imports
    
    def get_variables(self, source: str) -> List[Dict[str, Any]]:
        """
        Extract variable assignments from source code.
        
        Args:
            source: Python source code
            
        Returns:
            List of variable information
        """
        tree = self.parse(source)
        variables = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append({
                            'name': target.id,
                            'lineno': node.lineno,
                            'type': 'assign'
                        })
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    variables.append({
                        'name': node.target.id,
                        'lineno': node.lineno,
                        'type': 'annotated'
                    })
        
        self.analysis_count += 1
        return variables
    
    def get_calls(self, source: str) -> List[Dict[str, Any]]:
        """
        Extract function calls from source code.
        
        Args:
            source: Python source code
            
        Returns:
            List of function call information
        """
        tree = self.parse(source)
        calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                else:
                    func_name = '<unknown>'
                
                calls.append({
                    'name': func_name,
                    'lineno': node.lineno,
                    'num_args': len(node.args)
                })
        
        self.analysis_count += 1
        return calls
    
    def count_lines(self, source: str) -> int:
        """Count lines of code (excluding blank lines and comments)"""
        tree = self.parse(source)
        lines = set()
        
        for node in ast.walk(tree):
            if hasattr(node, 'lineno'):
                lines.add(node.lineno)
        
        return len(lines)
    
    def validate_syntax(self, source: str) -> bool:
        """
        Validate Python syntax.
        
        Args:
            source: Python source code
            
        Returns:
            True if valid syntax, False otherwise
        """
        try:
            self.parse(source)
            return True
        except SyntaxError:
            return False
    
    def fix_missing_locations(self, node: ast.AST) -> ast.AST:
        """
        Add missing line numbers and column offsets.
        
        Args:
            node: AST node
            
        Returns:
            Fixed AST node
        """
        return ast.fix_missing_locations(node)
    
    def increment_lineno(self, node: ast.AST, n: int = 1) -> ast.AST:
        """
        Increment line numbers in AST.
        
        Args:
            node: AST node
            n: Number to increment by
            
        Returns:
            Modified AST node
        """
        return ast.increment_lineno(node, n)
    
    def get_docstring(self, node: ast.AST) -> Optional[str]:
        """
        Get docstring from AST node.
        
        Args:
            node: AST node
            
        Returns:
            Docstring or None
        """
        return ast.get_docstring(node)
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'parsed': self.parse_count,
            'analyzed': self.analysis_count
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_operations': self.parse_count + self.analysis_count,
            'parse_operations': self.parse_count,
            'analysis_operations': self.analysis_count
        }
