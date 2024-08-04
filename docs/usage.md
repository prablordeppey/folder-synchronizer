# Usage

## Table of Contents

- [Simple Synchronization](#simple-synchronization)
- [Server-Based Synchronization](#server-based-synchronization)
- [Configuration](#configuration)
- [Example usage](#example-usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Documentation](#documentation)

### Simple Synchronization

The simple synchronization script continuously synchronizes a source folder with a replica folder at specified intervals using a while loop.

```sh
poetry run poe sync_simple
```

This command will start the synchronization process using the specified source and replica paths, synchronization interval, and log file path.

### Server-Based Synchronization

The server-based synchronization provides a REST API interface for more flexible and interactive synchronization management.

```sh
poetry run poe sync_server
```

This command will start the FastAPI server, allowing you to manage synchronization through HTTP requests.

### Configuration

**Command-Line Arguments**

- source: Path to the source folder that will be synchronized.
- --replica: Path to the replica folder that will be updated (optional).
- --interval: Synchronization interval in seconds (default: 60).
- --log_file: Path to the log file (default: logfile.log).

### Example usage:

To demonstrate the folder synchronization functionality, we will create a dummy source folder structure. This structure will be synchronized with a given replica path.

1. Create a `data` directory in your project root.
2. Inside the `data` directory, create a `source` directory.
3. Create the following file structure within the `source` directory:

    ```text
    data/
    └── source/
        ├── first_help.txt
        └── subfolder1/
            └── sub_first_help.txt
    └── output/
    ```

You can create this structure using the following python script
```python
import os

# Define the structure
structure = {
    "data": {
        "source": {
            "first_help.txt": "This is the first help file.",
            "subfolder1": {
                "sub_first_help.txt": "This is the subfolder first help file."
            }
        },
        "output": {}
    }
}

# Function to create the directory structure
def create_structure(base_path, structure):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, value)
        else:
            with open(path, "w") as file:
                file.write(value)

# Create the structure
base_path = os.getcwd()  # or specify the base path if different
create_structure(base_path, structure)
```

**Synchronizing Folders**

Simple Synchronization:

To run the simple synchronization script with the created folder structure:

```sh
poetry run poe sync_simple C:/path/to/your/project/data/source C:/path/to/your/project/data/replica 60 C:/path/to/your/project/data/logfile.log
```

Server-Based Synchronization:

To run the server-based synchronization with the created folder structure:

```sh
poetry run poe sync_server C:/path/to/your/project/data/source C:/path/to/your/project/data/replica 60 C:/path/to/your/project/data/logfile.log
```

Replace `C:/path/to/your/project` with the actual path to your project directory.

### API Endpoints
    
    - GET /: Returns the current synchronization count and CLI arguments.

    - GET /get_sync_params/: Returns the current synchronization parameters.

    - POST /update_sync_params/: Updates the synchronization parameters and restarts the synchronization job with the new parameters.

### Running Tests

To run tests with coverage, use the following commands:

```sh
poetry run poe test
```

or for detailed coverage reports:

```sh
poetry run poe test_cov
```

### Documentation

To serve the project documentation locally:

```sh
poetry run poe serve_docs
```

To build the project documentation:

```sh
poetry run poe build_docs
```