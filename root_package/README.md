# minor-utils

Utility library for formatting and function management.

## Installation

```bash
pip install minor-utils
```

## Modules

### Formatter
Format strings using built-in or custom formats. Supports pipelines, aliases, and enable/disable of formats.

```python
from minor_utils import Formatter

Formatter.formatting("hello world", "camelCase")  # "helloWorld"
Formatter.pipe("Hello World", "lower", "snake_case")  # "hello_world"
```

### Manager
Register and manage functions with a menu-based runner.

```python
from minor_utils import Manager

m = Manager()

@m.add_func
def greet():
    print("Hello!")

m.run_manual()
```

## Note

The project is in early development. APIs may change, bugs are possible.