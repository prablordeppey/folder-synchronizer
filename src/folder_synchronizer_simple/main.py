# src/folder_sync/main.py

import argparse
import time


from core.cli import ArgumentsModel
from core.logger import MainLogger
from core.synchronizer import FolderSynchronizer


def main() -> None:
    """
    Main entry point for the folder synchronization script for the simple case.

    This function sets up the argument parser for the script, which allows users to specify:
    - The path to the source folder that will be synchronized.
    - The path to the replica folder that will be updated.
    - The interval, in seconds, at which the synchronization should occur.
    - The path to the log file where synchronization activities will be recorded.

    The function performs the following steps:
    1. Parses command-line arguments to retrieve the source folder, replica folder, synchronization interval,
        and log file path.
    2. Configures logging based on the specified log file path using the `setup_logging` function.
    3. Logs an informational message indicating the start of synchronization, including the source and replica
        paths and the synchronization interval.
    4. Prints the parsed arguments to the console for user confirmation.

    Example usage:
        python script.py /path/to/source /path/to/replica 60 /path/to/logfile.log

    The function does not return any value.
    """
    parser = argparse.ArgumentParser(description="Synchronize source folder with replica folder.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("--replica", default=None, help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=60, help="Synchronization interval in seconds (default: 60)")
    parser.add_argument("--log_file", default=None, help="Path to the log file (default: logfile.log)")

    args = parser.parse_args()
    args_dict = vars(args)

    # Validate cli arguments
    args_model = ArgumentsModel(**args_dict)

    # Instantiate the logger
    logger = MainLogger("main", log_file=args_model.log_file, overwrite=True)

    logger.info(f"Parsed arguments:  {args_model}")
    logger.info(
        f"Starting synchronization: {args_model.source} -> {args_model.replica} every {args_model.interval} seconds"
    )

    while True:
        folder_synchronizer = FolderSynchronizer(logger=logger)
        folder_synchronizer.sync_folders(str(args_model.source), str(args_model.replica))
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
