import os
import stat
from typing_extensions import Optional
from pathlib import Path

from pydantic import BaseModel, DirectoryPath, PositiveInt, model_validator


class ArgumentsModel(BaseModel):
    """
    Model for command-line arguments.

    Attributes:
        source (DirectoryPath): Path to the source folder.
        replica (DirectoryPath): Path to the replica folder.
        interval (PositiveInt): Synchronization interval in seconds.
        log_file (Path): Path to the log file.

    Example:
        >>> args = ArgumentModel(
        >>>     source="/path/to/source",
        >>>     replica="/path/to/replica",
        >>>     interval=60,
        >>>     log_file="/path/to/logfile.log"
        >>> )
        >>> print(args)
        ArgumentsModel(source=PosixPath('/path/to/source'),
                       replica=PosixPath('/path/to/replica'),
                       interval=60,
                       log_file=Path('/path/to/logfile.log'))
    """

    source: DirectoryPath
    replica: Optional[DirectoryPath] = Path(os.getcwd(), "output", "replica")
    interval: Optional[PositiveInt] = 60
    log_file: Optional[Path] = Path(os.getcwd(), "output", "logfile.log")

    @model_validator(mode="before")
    def check_and_create__directories(cls, values: dict) -> dict:  # noqa: N805
        """
        Pre-validate after model is fully initialized.
        Permission update for 'source' and 'replica' folders.

        Args:
            cls: The class itself (used by Pydantic for validation).
            values (dict): A dictionary of field names and values.

        Returns:
            dict: The same dictionary of values after validation, with potential
                  side effects of creating the log file's parent directory.

        Raises:
            ValueError: If `log_file` is not specified in the `values` dictionary.
        """
        print("values:\n", values)
        log_file_path = values.get("log_file")
        source = values.get("source")
        replica = values.get("replica")

        # Check if source directory exists
        if not source or not source.exists():
            raise ValueError(f"The source directory '{source}' does not exist.")

        # Create replica directory if it does not exist
        if not replica:
            replica = Path(os.getcwd(), "output", "replica")
            values["replica"] = replica

        if not replica.is_absolute():
            raise ValueError(f"The path '{replica}' is not a full path.")

        if replica and not replica.exists():
            replica.mkdir(parents=True, exist_ok=True)

        # Ensure the parent directory of the log file exists
        if not log_file_path:
            log_file_path = Path(os.getcwd(), "output", "logfile.log")
            values["log_file"] = log_file_path

        if not log_file_path.exists():
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Update permissions
        cls.update_permissions(str(source))
        cls.update_permissions(str(replica))

        return values

    @staticmethod
    def update_permissions(path: str):
        """
        Update permissions of the given directory to ensure read and write access.

        Args:
            path (str): Path to the directory or file.

        Raises:
            ValueError: If the path is not a directory.
        """
        # Set permissions to 755 (read/write/execute for owner, read/execute for group/others)
        for root, dirs, files in os.walk(path):
            for d in dirs:
                dir_path = os.path.join(root, d)
                os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
            for f in files:
                file_path = os.path.join(root, f)
                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
