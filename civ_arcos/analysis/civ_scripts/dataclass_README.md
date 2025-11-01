# DataClass - Structured Data Builder

Structured data type creator for Python development.

## Description

DataClass provides functionality for creating and managing dataclasses.

## Usage

```python
from civ_arcos.analysis.civ_scripts.dataclass import DataClass

dc = DataClass()

# Create a simple dataclass
Person = dc.make_simple("Person", name=str, age=int, email=str)
person = Person(name="Alice", age=30, email="alice@example.com")

# Convert to dictionary
person_dict = dc.to_dict(person)

# Convert to tuple
person_tuple = dc.to_tuple(person)

# Create new instance with modifications
person2 = dc.replace(person, age=31)

# Get field information
fields = dc.get_fields(Person)
field_names = dc.get_field_names(Person)
field_types = dc.get_field_types(Person)

# Use decorator for manual class definition
@dc.decorator(frozen=True, order=True)
class Point:
    x: int
    y: int
```

## Features

- Dynamic dataclass creation
- Field customization
- Instance conversion (dict, tuple)
- Instance modification (immutable replacement)
- Field introspection
- Frozen (immutable) dataclasses
- Ordered dataclasses
- Default values and factories

## API Reference

### Creation Methods

- `make(name, fields, frozen=False, order=False)` - Create dataclass dynamically
- `make_simple(class_name, **field_types)` - Create simple dataclass
- `make_from_dict(name, data, frozen=False)` - Create from dictionary with type inference
- `decorator(init=True, repr=True, ...)` - Get dataclass decorator

### Field Methods

- `field(default, default_factory, ...)` - Create field with options
- `get_fields(class_or_instance)` - Get fields from dataclass
- `get_field_names(class_or_instance)` - Get list of field names
- `get_field_types(class_or_instance)` - Get dictionary of field types

### Instance Methods

- `to_dict(instance, dict_factory=dict)` - Convert instance to dictionary
- `to_tuple(instance, tuple_factory=tuple)` - Convert instance to tuple
- `replace(instance, **changes)` - Create new instance with modifications
- `is_dataclass(obj)` - Check if object is a dataclass
- `validate_instance(instance)` - Validate instance matches definition

## Examples

### Basic Usage

```python
# Create a dataclass
Point = dc.make_simple("Point", x=int, y=int)
p = Point(x=10, y=20)

# Convert to dict
print(dc.to_dict(p))  # {'x': 10, 'y': 20}
```

### Frozen Dataclass

```python
# Create immutable dataclass
Config = dc.make("Config", [("name", str), ("value", int)], frozen=True)
cfg = Config(name="debug", value=1)
# cfg.value = 2  # Would raise FrozenInstanceError
```

### Custom Fields

```python
# Use field with default factory
from civ_arcos.analysis.civ_scripts.dataclass import DataClass

dc = DataClass()
default_field = dc.field(default_factory=list)
```

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.dataclass
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
