# PathFinder - Path Utility

Path handler for Python development using pathlib.

## Description

PathFinder provides functionality for handling file paths and operations with an enhanced interface around Python's pathlib module.

## Usage

```python
from civ_arcos.analysis.civ_scripts.pathfinder import PathFinder

pf = PathFinder()

# Create path
path = pf.path("home", "user", "documents")

# Join paths
full_path = pf.join("/home/user", "documents", "file.txt")

# Check existence
if pf.exists(full_path):
    print("File exists")

# Read/write text files
text = pf.read_text("input.txt")
pf.write_text("output.txt", "Hello, World!")

# Directory operations
pf.mkdir("new_directory", parents=True, exist_ok=True)
files = pf.listdir(".")

# File operations
pf.copy("source.txt", "backup.txt")
pf.move("old_location.txt", "new_location.txt")
```

## Features

- Path creation and manipulation
- File and directory operations
- Existence and type checking
- Read/write operations (text and binary)
- File metadata (size, modification time)
- Glob pattern matching
- Directory walking
- Statistics tracking

## API Reference

### Constructor

- `PathFinder()` - Initialize path finder

### Path Creation Methods

- `path(*args)` - Create Path object
- `join(*parts)` - Join path components
- `absolute(path)` - Get absolute path
- `resolve(path)` - Resolve path (absolute + resolve symlinks)

### Checking Methods

- `exists(path)` - Check if path exists
- `is_file(path)` - Check if path is a file
- `is_dir(path)` - Check if path is a directory
- `is_absolute(path)` - Check if path is absolute

### Path Component Methods

- `parent(path)` - Get parent directory
- `name(path)` - Get file/directory name
- `stem(path)` - Get filename without extension
- `suffix(path)` - Get file extension
- `suffixes(path)` - Get all file extensions
- `parts(path)` - Get path components as tuple

### Directory Operations

- `mkdir(path, parents=False, exist_ok=False)` - Create directory
- `rmdir(path)` - Remove empty directory
- `listdir(path='.')` - List directory contents
- `glob(path, pattern)` - Find files matching pattern
- `rglob(path, pattern)` - Recursively find files matching pattern
- `walk(path)` - Walk directory tree

### File Operations

- `touch(path, exist_ok=True)` - Create empty file
- `unlink(path, missing_ok=False)` - Remove file
- `rename(path, target)` - Rename file or directory
- `replace(path, target)` - Replace file or directory
- `copy(src, dst)` - Copy file
- `copytree(src, dst)` - Copy directory tree
- `move(src, dst)` - Move file or directory

### Read/Write Methods

- `read_text(path, encoding='utf-8')` - Read text file
- `read_bytes(path)` - Read binary file
- `write_text(path, data, encoding='utf-8')` - Write text file
- `write_bytes(path, data)` - Write binary file

### Metadata Methods

- `size(path)` - Get file size in bytes
- `mtime(path)` - Get modification time

### System Methods

- `cwd()` - Get current working directory
- `home()` - Get user home directory
- `expanduser(path)` - Expand ~ in path

### Statistics Methods

- `get_results()` - Get processing results
- `get_statistics()` - Get detailed statistics
- `clear_history()` - Clear operation history

## Examples

### Basic Path Operations

```python
pf = PathFinder()

# Create and manipulate paths
path = pf.path("/home/user/documents")
file_path = pf.join(path, "report.pdf")

print(pf.name(file_path))   # "report.pdf"
print(pf.stem(file_path))   # "report"
print(pf.suffix(file_path)) # ".pdf"
print(pf.parent(file_path)) # "/home/user/documents"
```

### File Existence and Type

```python
pf = PathFinder()

if pf.exists("config.json"):
    if pf.is_file("config.json"):
        print("It's a file")
    elif pf.is_dir("config.json"):
        print("It's a directory")
```

### Directory Management

```python
pf = PathFinder()

# Create directory structure
pf.mkdir("project/src/utils", parents=True, exist_ok=True)

# List contents
files = pf.listdir("project/src")
for file in files:
    print(file)

# Remove directory
pf.rmdir("project/temp")
```

### File Reading and Writing

```python
pf = PathFinder()

# Write text file
pf.write_text("notes.txt", "Important notes here")

# Read text file
content = pf.read_text("notes.txt")

# Write binary file
pf.write_bytes("data.bin", b"\x00\x01\x02\x03")

# Read binary file
binary_data = pf.read_bytes("data.bin")
```

### File Operations

```python
pf = PathFinder()

# Create empty file
pf.touch("newfile.txt")

# Copy file
pf.copy("source.txt", "backup.txt")

# Move file
pf.move("oldname.txt", "newname.txt")

# Delete file
pf.unlink("tempfile.txt", missing_ok=True)
```

### Pattern Matching

```python
pf = PathFinder()

# Find all Python files in directory
py_files = pf.glob(".", "*.py")
for file in py_files:
    print(file)

# Recursively find all JSON files
json_files = pf.rglob(".", "**/*.json")
for file in json_files:
    print(file)
```

### Directory Walking

```python
pf = PathFinder()

# Walk through directory tree
for dirpath, dirnames, filenames in pf.walk("project"):
    print(f"Directory: {dirpath}")
    for filename in filenames:
        full_path = pf.join(dirpath, filename)
        print(f"  File: {full_path}")
```

### Path Resolution

```python
pf = PathFinder()

# Get absolute path
abs_path = pf.absolute("relative/path/file.txt")

# Resolve path (follow symlinks)
real_path = pf.resolve("link_to_file.txt")

# Expand home directory
home_path = pf.expanduser("~/documents")
```

### File Metadata

```python
pf = PathFinder()

# Get file size
file_size = pf.size("largefile.bin")
print(f"Size: {file_size} bytes")

# Get modification time
mod_time = pf.mtime("document.txt")
print(f"Last modified: {mod_time}")
```

### System Paths

```python
pf = PathFinder()

# Get current working directory
current = pf.cwd()
print(f"Current directory: {current}")

# Get home directory
home = pf.home()
print(f"Home directory: {home}")
```

### Statistics

```python
pf = PathFinder()

# Perform various operations
pf.mkdir("temp")
pf.write_text("temp/file.txt", "data")
pf.copy("temp/file.txt", "temp/backup.txt")

stats = pf.get_statistics()
# {
#   'total_operations': 3,
#   'operation_types': {'mkdir': 1, 'write_text': 1, 'copy': 1}
# }

# Clear history
pf.clear_history()
```

## Advanced Features

### Path Arithmetic

```python
pf = PathFinder()

# Join paths with / operator
base = pf.path("/home/user")
full_path = base / "documents" / "file.txt"
```

### Multiple Suffixes

```python
pf = PathFinder()

path = pf.path("archive.tar.gz")
print(pf.suffix(path))   # ".gz"
print(pf.suffixes(path)) # [".tar", ".gz"]
```

### Safe File Operations

```python
pf = PathFinder()

# Create directory, don't fail if exists
pf.mkdir("logs", exist_ok=True)

# Delete file, don't fail if missing
pf.unlink("tempfile.txt", missing_ok=True)

# Create file, don't fail if exists
pf.touch("lockfile", exist_ok=True)
```

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.pathfinder
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
