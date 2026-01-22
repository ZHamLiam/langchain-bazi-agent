# Agents Guide for langchain_bazi_agent

This document provides guidelines for agentic coding assistants working in this repository.

## Build, Lint, and Test Commands

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific_module.py

# Run specific test function
pytest tests/test_specific_module.py::test_function_name

# Run tests with coverage
pytest --cov=src

# Run tests matching a pattern
pytest -k "test_pattern"
```

### Linting and Formatting
```bash
# Format code with Black
black .

# Check formatting without modifying
black --check .

# Lint with Ruff
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Type checking with mypy
mypy src/

# Import sorting with isort
isort .

# Check imports without modifying
isort --check-only .
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt

# Add new dependency (use poetry if applicable)
poetry add package_name

# Install specific LangChain version
pip install langchain==1.2.6
```

**Important:** This project requires LangChain version 1.2.6. When installing dependencies, ensure this exact version is used.

## Code Style Guidelines

### Python Conventions

#### Imports
- Use absolute imports over relative imports when possible
- Group imports in this order: stdlib, third-party, local
- Separate groups with a blank line
- Use `from module import Thing` for frequently used names
- Use `import module` for infrequently used names

```python
# Correct
import os
from typing import List, Optional
from langchain.chains import Chain
from myproject.utils import helper_function

# Avoid
from myproject.utils import *
import os
from langchain.chains import Chain
```

#### Formatting
- Use Black formatter (maximum line length: 88)
- Use 4 spaces for indentation (no tabs)
- Trailing commas in multi-line function definitions and data structures

```python
def function_name(
    arg1: str,
    arg2: int,
    arg3: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {"result": arg1 + str(arg2)}
```

#### Type Hints
- Type all function arguments and return values
- Use `Optional[T]` for nullable types
- Use `Union[T, None]` instead of `Optional` for type checkers
- Use type aliases for complex types
- Use `List`, `Dict`, `Set` from typing module

```python
from typing import List, Dict, Optional, Any, TypeVar

T = TypeVar('T')

def process_items(items: List[T]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for item in items:
        result[str(item)] = item
    return result
```

#### Naming Conventions
- Classes: PascalCase (`MyClass`)
- Functions and methods: snake_case (`my_function`)
- Variables: snake_case (`my_variable`)
- Constants: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- Private methods: prefix with underscore (`_private_method`)
- Protected attributes: prefix with single underscore (`_protected`)
- Module level "dunders": use sparingly (`__all__`, `__version__`)

#### Error Handling
- Use specific exceptions rather than generic `Exception`
- Use `raise` with descriptive messages
- Use `try/except/finally` for cleanup
- Use context managers for resource management

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except (KeyError, IndexError) as e:
    logger.warning(f"Missing data: {e}")
    return {}
finally:
    cleanup_resources()
```

#### Docstrings
- Use Google-style docstrings or reStructuredText
- Include description, args, returns, and raises sections
- Document public functions and classes

```python
def calculate_mean(values: List[float]) -> float:
    """Calculate the arithmetic mean of a list of values.

    Args:
        values: List of numeric values.

    Returns:
        The arithmetic mean of the input values.

    Raises:
        ValueError: If the input list is empty.
    """
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)
```

### LangChain-Specific Guidelines

- Use type hints for LangChain components
- Prefer composition over inheritance
- Use proper error handling for chain execution
- Document custom prompts and chains
- Use `Runnable` protocol for chain components

```python
from langchain_core.runnables import Runnable

class CustomProcessor(Runnable):
    """Custom processing chain component."""

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data."""
        # Implementation
        return processed_data
```

### File Structure
- Place main application code in `src/` directory
- Unit tests in `tests/` directory mirroring source structure
- Configuration files in root directory
- Documentation in `docs/` directory

### Logging
- Use Python's `logging` module
- Configure appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Include context in log messages
- Avoid logging sensitive data

### Best Practices
- Keep functions focused and small (< 50 lines preferred)
- Use list comprehensions for simple transformations
- Prefer generator expressions over list comprehensions for large datasets
- Use `dataclasses` or `pydantic` models for data structures
- Write tests before implementation when adding features
- Keep modules under 500 lines when possible
- Use dependency injection for testability
