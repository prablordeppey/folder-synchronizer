# Usage

## Pre-requisite

You should have `poetry` already installed in your environment.

## Installation

Install the base dependencies:

```sh
poetry install
```

Install the dependencies for the simple implementation:

```sh
poe install_simple
```

Install the dependencies for the server implementation:

```sh
poe install_simple
```

## Running the Synchronizer
To run the synchronizer:

```sh
poe sync_simple
```

## Running tests with coverage
To run the tests:

```sh
poe test
```

## Example `api_reference.md`:

```markdown
# API Reference

## MainLogger

```python
from src.core.logger import MainLogger
```