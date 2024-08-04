import time

from core.cli import arguments_parser
from core.logger import MainLogger
from core.synchronizer import FolderSynchronizer
from core.utils import setup_parent_dirs


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
        >> python script.py /path/to/source /path/to/replica 60 /path/to/logfile.log

    The function does not return any value.
    """

    # Grab cli arguments
    args_model = arguments_parser()

    source = args_model.source
    replica = args_model.replica
    log_file = args_model.log_file
    interval = args_model.interval

    # Instantiate the logger
    logger = MainLogger("simple_main", log_file=log_file, overwrite=True)
    logger.info(f"Parsed arguments:  {args_model}")

    # Setup parent directories
    logger.info("Setting-up parent directories ...")
    setup_parent_dirs(args_model, logger)

    logger.info(f"Starting synchronization: {source} -> {replica} every {interval} seconds")

    while True:
        folder_synchronizer = FolderSynchronizer(logger=logger)
        folder_synchronizer.sync_folders(source, replica)
        time.sleep(interval)


if __name__ == "__main__":
    main()
