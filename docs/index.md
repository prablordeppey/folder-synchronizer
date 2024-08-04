# Folder Synchronizer

Welcome to the Folder Synchronizer documentation.

**Folder Synchronizer** is a versatile Python application designed to synchronize directories either through a simple command-line script or via a RESTful API server. 

## Features

- **Simple Synchronization Script**: Utilizes a command-line interface (CLI) with a while loop to continuously synchronize a source folder with a replica folder at specified intervals. It supports logging to a file and allows users to configure synchronization parameters through CLI arguments.

- **REST API Server**: Provides a web server using FastAPI for advanced functionality. It allows dynamic updates to synchronization parameters via API endpoints, such as adjusting synchronization intervals and retrieving current settings. It leverages background tasks to manage synchronization according to the configured intervals.

## Components

- **`folder_synchronizer_simple`**: Implements a straightforward synchronization process using a while loop and sleep intervals, suitable for basic use cases where continuous synchronization is needed.

- **`folder_synchronizer_server`**: Offers a REST API interface for more flexible and interactive synchronization management, ideal for integration into larger systems or for users who prefer managing synchronization through HTTP requests.

The project combines practical synchronization capabilities with robust logging and configuration management, making it adaptable for various use cases and environments.
