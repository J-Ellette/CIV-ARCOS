# Submarine - Subprocess runner

Process manager for Python development.

## Description

Submarine provides functionality to run commands.

## Usage

```python
from Submarine import Submarine

tool = Submarine()
tool.process('item')
results = tool.get_results()
```

## Features

- Process items efficiently
- Track statistics
- Get results

## API Reference

- `__init__()` - Initialize tool
- `process(item)` - Process an item
- `get_results()` - Get processing results
- `get_statistics()` - Get statistics

## Testing

```bash
python test_Submarine.py
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
