# Folder Synchronizer

Folder Synchronizer is a versatile Python application designed to synchronize directories either through a simple command-line script or via a RESTful API server.

## Table of Contents

- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Creating the Virtual Environment](#creating-the-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)

## Setup and Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.12
- Poetry

### Creating the Virtual Environment

To create a virtual environment and install Poetry, run:

```sh
poetry run poe create_venv
```

### Installing Dependencies

**Development Dependencies**

To install all dependencies required for development, run:

```sh
poetry run poe install_dev
```

**Simple Synchronization Dependencies**

To install dependencies for the simple synchronization script, excluding server dependencies, run:

```sh
poetry run poe install_simple
```

**Server-Based Synchronization Dependencies**

To install dependencies for the server-based synchronization, including server dependencies, run:

```sh
poetry run poe install_server
```

**All Dependencies**

To install all dependencies, run:

```sh
poetry run poe install_all
```

**Cleaning Up**

To remove all Poetry-created virtual environments and clear the cache, run:

```sh
poetry run poe clean
```
