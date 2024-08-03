import os
import shutil
import filecmp

from typing import Optional

from core.logger import MainLogger


class FolderSynchronizer:
    """
    A class to synchronize two folders: source and replica.

    Attributes:
        logger (logging.Logger): Logger instance for logging operations.
    """

    def __init__(self, logger: Optional[MainLogger] = None) -> None:
        """
        Initialize the FolderSynchronizer.

        Args:
            logger (Optional[logging.Logger]): Logger instance for logging operations.
        """
        self.logger = logger if logger else MainLogger(name=__name__)
        self.logger.info("Synchronizer initialized.")

    def sync_folders(self, source_path: str, replica_path: str):
        """
        Recursively synchronize the source folder with the replica folder.

        This helper function ensures that the contents of the source directory are mirrored in the replica directory.
        It handles both the copying of new or updated files and the removal of excess files and directories.

        Details:
            - **Directory Synchronization**:
                - If `source_item` is a directory, the function is called recursively for each subdirectory and file.
                - If `replica_item` is missing or outdated compared to `source_item`, it will be updated or created.

            - **File Synchronization**:
                - Files are copied from `source_item` to `replica_item` if they do not exist in the replica directory
                    or if their contents differ.
                - Uses `filecmp.cmp()` with `shallow=False` to ensure that files are compared based on their contents,
                    not just metadata.

            - **Removal of Excess Files and Directories**:
                - Any files or directories in `replica_item` that do not exist in `source_item` are removed.
                - Directories and files are deleted from the replica location as needed to maintain synchronization
                    with the source.

        Logging:
            - Logs the copying of files from the source to the replica directory.
            - Logs the removal of excess files and directories from the replica directory.

        Exceptions:
            - May raise exceptions related to file system operations such as
                `FileNotFoundError`, `PermissionError`, or `OSError`.

        Example:
            >>> self.sync_folders_recursive("/path/to/source", "/path/to/replica")
        """
        # Synchronize files and directories from source_item to replica_item.
        self.logger.info("Copying source files and dirs to replica ...")
        for item in os.listdir(source_path):
            source_sub_item = os.path.join(source_path, item)
            replica_sub_item = os.path.join(replica_path, item)

            self.logger.debug(f"working on {item}")

            if os.path.isdir(source_sub_item):
                if not os.path.exists(replica_sub_item):
                    os.makedirs(replica_sub_item)
                self.sync_folders(source_sub_item, replica_sub_item)
            else:
                if not os.path.exists(replica_sub_item) or not filecmp.cmp(
                    source_sub_item, replica_sub_item, shallow=False
                ):
                    self.logger.debug(f"Copying file {source_sub_item} to {replica_sub_item}")
                    shutil.copy2(source_sub_item, replica_sub_item)

        # Remove excess files and directories from replica_item.
        self.logger.info("Remove unwanted replica files and dirs ...")
        for item in os.listdir(replica_path):
            source_sub_item = os.path.join(source_path, item)
            replica_sub_item = os.path.join(replica_path, item)

            self.logger.debug(f"working on {item}")

            if not os.path.exists(source_sub_item):
                if os.path.isdir(replica_sub_item):
                    self.logger.debug(f"Removing directory {replica_sub_item}")
                    shutil.rmtree(replica_sub_item, ignore_errors=True)
                else:
                    self.logger.debug(f"Removing file {replica_sub_item}")
                    os.remove(replica_sub_item)
