# Jason - JSON Processor

JSON processor for Python development using json.

## Description

Jason provides functionality for parsing, validating, and serializing JSON data with enhanced error handling.

## Usage

```python
from civ_arcos.analysis.civ_scripts.jason import Jason

jason = Jason()

# Parse JSON string
data = jason.loads('{"name": "Alice", "age": 30}')
print(data["name"])  # Alice

# Serialize to JSON
json_string = jason.dumps({"name": "Bob", "age": 25}, indent=2)
print(json_string)

# Load from file
data = jason.load("config.json")

# Save to file
jason.dump({"setting": "value"}, "output.json")

# Validate JSON
is_valid = jason.validate('{"valid": true}')

# Prettify JSON
pretty = jason.prettify('{"a":1,"b":2}')

# Minify JSON
compact = jason.minify('{\n  "a": 1\n}')
```

## Features

- JSON parsing (string and file)
- JSON serialization (string and file)
- JSON validation
- Pretty printing and minification
- JSON merging
- Diff between JSON objects
- Error tracking
- Statistics

## API Reference

### Constructor

- `Jason()` - Initialize JSON processor

### Parsing Methods

- `loads(json_string, strict=True, **kwargs)` - Parse JSON from string
- `load(file, **kwargs)` - Load JSON from file

### Serialization Methods

- `dumps(obj, indent=None, sort_keys=False, ensure_ascii=True, **kwargs)` - Serialize to JSON string
- `dump(obj, file, indent=2, sort_keys=False, **kwargs)` - Dump object to JSON file

### Validation Methods

- `validate(json_string)` - Check if string is valid JSON

### Formatting Methods

- `prettify(json_string, indent=2, sort_keys=False)` - Format JSON with indentation
- `minify(json_string)` - Remove whitespace from JSON

### Utility Methods

- `merge(*json_objects)` - Merge multiple JSON objects
- `diff(obj1, obj2)` - Find differences between two objects

### Statistics Methods

- `get_results()` - Get processing results
- `get_statistics()` - Get detailed statistics
- `get_errors()` - Get error history
- `clear_errors()` - Clear error history

## Examples

### Basic Parsing

```python
jason = Jason()
data = jason.loads('{"name": "Alice", "items": [1, 2, 3]}')
print(data["name"])  # Alice
print(data["items"]) # [1, 2, 3]
```

### File Operations

```python
jason = Jason()

# Load from file
config = jason.load("config.json")

# Save to file
jason.dump({"version": "1.0", "debug": True}, "settings.json")
```

### Pretty Printing

```python
jason = Jason()
compact = '{"name":"Bob","age":30,"city":"NYC"}'
pretty = jason.prettify(compact, indent=4)
print(pretty)
# {
#     "age": 30,
#     "city": "NYC",
#     "name": "Bob"
# }
```

### Minification

```python
jason = Jason()
formatted = '''
{
  "key": "value",
  "number": 123
}
'''
compact = jason.minify(formatted)
print(compact)  # {"key":"value","number":123}
```

### Validation

```python
jason = Jason()
is_valid = jason.validate('{"valid": true}')  # True
is_valid = jason.validate('{invalid}')        # False
```

### Merging Objects

```python
jason = Jason()
obj1 = {"a": 1, "b": 2}
obj2 = {"b": 3, "c": 4}
obj3 = {"d": 5}

merged = jason.merge(obj1, obj2, obj3)
# {'a': 1, 'b': 3, 'c': 4, 'd': 5}
```

### Finding Differences

```python
jason = Jason()
old_config = {"host": "localhost", "port": 8080, "debug": True}
new_config = {"host": "0.0.0.0", "port": 8080, "ssl": True}

diff = jason.diff(old_config, new_config)
# {
#   'added': ['ssl'],
#   'removed': ['debug'],
#   'changed': [{'key': 'host', 'old': 'localhost', 'new': '0.0.0.0'}]
# }
```

### Error Handling

```python
jason = Jason()

try:
    jason.loads('{invalid json}')
except json.JSONDecodeError as e:
    print(f"Parse error: {e}")

# Check error history
errors = jason.get_errors()
print(f"Total errors: {len(errors)}")

# Clear error history
jason.clear_errors()
```

### Statistics

```python
jason = Jason()
jason.loads('{"a": 1}')
jason.dumps({"b": 2})
jason.load("file.json")
jason.dump({"c": 3}, "out.json")

stats = jason.get_statistics()
# {
#   'total_operations': 4,
#   'parse_operations': 2,
#   'serialize_operations': 2,
#   'error_count': 0
# }
```

## Advanced Usage

### Custom Serialization

```python
jason = Jason()

# Sort keys alphabetically
json_str = jason.dumps({"z": 1, "a": 2}, sort_keys=True)

# Compact separators
json_str = jason.dumps({"a": 1}, separators=(',', ':'))

# Handle non-ASCII characters
json_str = jason.dumps({"text": "こんにちは"}, ensure_ascii=False)
```

### Path-like Objects

```python
from pathlib import Path

jason = Jason()

# Load from Path object
data = jason.load(Path("config.json"))

# Save to Path object
jason.dump(data, Path("output.json"))
```

## Error Tracking

Jason tracks all parsing and serialization errors:

```python
jason = Jason()

# Trigger some errors
try:
    jason.loads("{bad json}")
except:
    pass

# View errors
errors = jason.get_errors()
for error in errors:
    print(f"Error: {error}")

# Clear error log
jason.clear_errors()
```

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.jason
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
