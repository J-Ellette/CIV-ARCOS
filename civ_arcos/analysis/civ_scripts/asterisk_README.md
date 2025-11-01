# Asterisk - AST Parser

Abstract Syntax Tree parser for Python development.

## Description

Asterisk provides functionality for parsing and analyzing Python source code using Abstract Syntax Trees (AST).

## Usage

```python
from civ_arcos.analysis.civ_scripts.asterisk import Asterisk

parser = Asterisk()

# Parse source code
code = """
def hello():
    return "world"
"""
tree = parser.parse(code)

# Extract functions
functions = parser.get_functions(code)
print(f"Functions: {[f['name'] for f in functions]}")

# Extract classes
classes = parser.get_classes(code)

# Extract imports
imports = parser.get_imports(code)

# Validate syntax
is_valid = parser.validate_syntax(code)
```

## Features

- Parse Python source code into AST
- Extract function definitions
- Extract class definitions
- Extract import statements
- Extract variable assignments
- Extract function calls
- Validate Python syntax
- Count lines of code
- Convert AST back to source code
- Safely evaluate literal expressions

## API Reference

### Main Methods

- `parse(source, filename='<string>', mode='exec')` - Parse Python source into AST
- `parse_file(filepath)` - Parse Python file into AST
- `dump(node, ...)` - Dump AST as string
- `unparse(node)` - Convert AST back to source code
- `literal_eval(source)` - Safely evaluate literal expressions
- `walk(node)` - Walk all nodes in AST

### Analysis Methods

- `get_functions(source)` - Extract function definitions
- `get_classes(source)` - Extract class definitions
- `get_imports(source)` - Extract import statements
- `get_variables(source)` - Extract variable assignments
- `get_calls(source)` - Extract function calls
- `count_lines(source)` - Count lines of code
- `validate_syntax(source)` - Validate Python syntax
- `get_docstring(node)` - Get docstring from AST node

### Utility Methods

- `fix_missing_locations(node)` - Add missing line numbers
- `increment_lineno(node, n)` - Increment line numbers

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.asterisk
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
