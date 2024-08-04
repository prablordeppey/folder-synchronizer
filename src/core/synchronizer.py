import os
import shutil
import filecmp
from pathlib import Path
from typing import Optional

from core.logger import MainLogger


class FolderSynchronizer:
    """
    A class responsible for synchronizing the contents of a source folder with a replica folder.

    This class provides functionality to ensure that the `replica` folder mirrors the `source` folder by copying new
    or updated files and directories, and removing any that are no longer present in the source.

    Attributes:
        logger (MainLogger): Logger instance for recording operations and events.
    """

    def __init__(self, logger: Optional[MainLogger] = None) -> None:
        """
        Initialize the FolderSynchronizer with an optional logger.

        Args:
            logger (Optional[MainLogger]): An optional `MainLogger` instance for logging operations. If not provided,
                                           a default logger is created.
        """
        self.logger = logger if logger else MainLogger(name=__name__)
        self.logger.info("Synchronizer initialized.")

    def sync_folders(self, source_path: Path, replica_path: Path):
        """
        Recursively synchronize the `replica` folder to match the `source` folder.

        This method performs a two-way synchronization:

        1. **Copying Files and Directories**:
            - Recursively copies new or updated files and directories from `source_path` to `replica_path`.
            - Directories are created in the replica if they do not exist.
            - Files are copied only if they are missing or different from the source.

        2. **Removing Excess Files and Directories**:
            - Deletes files and directories from `replica_path` that are not present in `source_path`.

        Logging:
            - Logs details about copying files, creating directories, and removing excess files and directories.

        Exceptions:
            - May raise `FileNotFoundError`, `PermissionError`, or `OSError` if issues occur during file operations.

        Args:
            source_path (Path): The path to the source directory.
            replica_path (Path): The path to the replica directory.

        Example:
            >>> synchronizer = FolderSynchronizer()

            >>> synchronizer.sync_folders(Path("/path/to/source"), Path("/path/to/replica"))
        """
        # Synchronize files and directories from source_path to replica_path.
        self.logger.info("Synchronizing source files and directories to replica...")
        for item in os.listdir(source_path):
            source_sub_item = Path(source_path, item)
            replica_sub_item = Path(replica_path, item)

            self.logger.debug(f"Processing {item}")

            if source_sub_item.is_dir():
                if not replica_sub_item.exists():
                    self.logger.debug(f"Directory not found in replica: {replica_sub_item}")
                    self.logger.debug(f"Creating directory: {replica_sub_item}")
                    replica_sub_item.mkdir(parents=True, exist_ok=True)
                self.sync_folders(source_sub_item, replica_sub_item)
            else:
                if not replica_sub_item.exists() or not filecmp.cmp(source_sub_item, replica_sub_item, shallow=False):
                    self.logger.debug(f"File '{source_sub_item}' differs or is missing in replica.")
                    self.logger.debug(f"Copying file: {source_sub_item}")
                    shutil.copy2(source_sub_item, replica_sub_item)

        # Remove excess files and directories from replica_path.
        self.logger.info("Removing excess files and directories from replica...")
        for item in os.listdir(replica_path):
            source_sub_item = Path(source_path, item)
            replica_sub_item = Path(replica_path, item)

            self.logger.debug(f"Processing {item}")

            if not source_sub_item.exists():
                if replica_sub_item.is_dir():
                    self.logger.debug(f"Directory in replica not found in source: {replica_sub_item}")
                    self.logger.debug(f"Removing directory: {replica_sub_item}")
                    shutil.rmtree(replica_sub_item, ignore_errors=True)
                else:
                    self.logger.debug(f"File in replica not found in source: {replica_sub_item}")
                    self.logger.debug(f"Removing file: {replica_sub_item}")
                    os.remove(replica_sub_item)
