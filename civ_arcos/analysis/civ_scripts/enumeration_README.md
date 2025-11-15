# Enumeration - Enum Builder

Enumeration type creator for Python development.

## Description

Enumeration provides functionality for creating and managing enum types.

## Usage

```python
from civ_arcos.analysis.civ_scripts.enumeration import Enumeration

enumerator = Enumeration()

# Create a simple enum
Color = enumerator.make_simple("Color", "RED", "GREEN", "BLUE")

# Access members
red = Color.RED
print(red.name)   # "RED"
print(red.value)  # 1 (auto-assigned)

# Lookup by name
red = enumerator.lookup_by_name(Color, "RED")

# Lookup by value
color = enumerator.lookup_by_value(Color, 1)

# Get all members
members = enumerator.get_member_names(Color)
values = enumerator.get_member_values(Color)

# Create IntEnum with specific values
Status = enumerator.make_int("Status", {"OK": 200, "NOT_FOUND": 404})
```

## Features

- Dynamic enum creation
- IntEnum support
- Flag enum support
- IntFlag support
- Member lookup by name/value
- Member introspection
- Enum extension
- Unique value enforcement

## API Reference

### Creation Methods

- `make(name, members, enum_type=Enum)` - Create enum dynamically
- `make_simple(name, *members)` - Create simple enum with auto values
- `make_int(name, members)` - Create IntEnum
- `make_flag(name, *members)` - Create Flag enum
- `make_int_flag(name, members)` - Create IntFlag enum
- `from_dict(name, data)` - Create enum from dictionary
- `extend(base_enum, name, new_members)` - Create extended enum

### Lookup Methods

- `lookup_by_name(enum_class, name)` - Lookup member by name
- `lookup_by_value(enum_class, value)` - Lookup member by value
- `has_member(enum_class, name)` - Check if member exists
- `has_value(enum_class, value)` - Check if value exists

### Introspection Methods

- `get_members(enum_class)` - Get all members
- `get_member_names(enum_class)` - Get list of member names
- `get_member_values(enum_class)` - Get list of member values
- `get_name(member)` - Get name of member
- `get_value(member)` - Get value of member
- `is_member(obj)` - Check if object is enum member
- `to_dict(enum_class)` - Convert enum to dictionary

### Utility Methods

- `unique_decorator()` - Get @unique decorator
- `auto_value()` - Get auto() function
- `compare(member1, member2)` - Compare enum members

## Examples

### Basic Usage

```python
# Create and use enum
Color = enumerator.make_simple("Color", "RED", "GREEN", "BLUE")
print(Color.RED)  # Color.RED
```

### IntEnum

```python
# HTTP status codes
Status = enumerator.make_int("Status", {
    "OK": 200,
    "CREATED": 201,
    "NOT_FOUND": 404
})
print(Status.OK == 200)  # True
```

### Flag Enum

```python
# Permission flags
Permission = enumerator.make_flag("Permission", "READ", "WRITE", "EXECUTE")
# Can combine with | operator
```

### Extending Enum

```python
# Extend existing enum
BasicColor = enumerator.make_simple("BasicColor", "RED", "GREEN", "BLUE")
ExtendedColor = enumerator.extend(
    BasicColor, 
    "ExtendedColor",
    {"YELLOW": 4, "PURPLE": 5}
)
```

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.enumeration
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
