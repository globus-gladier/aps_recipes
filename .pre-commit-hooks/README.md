# Pre-commit Hooks

This directory contains custom pre-commit hooks for the repository.

## Recipe Validation

The `validate_recipes.py` script validates `.recipe` files for common issues and best practices. It checks for:

- Presence of FROM instruction
- Valid base image format (must use fully qualified names)
- Proper formatting of multi-line RUN commands
- Proper cleanup after package manager commands (apt-get, conda)
- Presence of CMD or ENTRYPOINT instruction

## Setup

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. (Optional) Run the hooks on all files:
   ```bash
   pre-commit run --all-files
   ```

## Manual Validation

You can also run the recipe validation manually:

```bash
python .pre-commit-hooks/validate_recipes.py path/to/recipe.recipe
```

## Requirements

- Python 3.11+
- pre-commit
- dockerfile-parse
