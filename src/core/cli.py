import argparse
from functools import lru_cache
import os
import stat
from typing import Annotated
from pathlib import Path

from pydantic import BaseModel, DirectoryPath, Field, model_validator


class ArgumentsModel(BaseModel):
    """
    Model for command-line arguments.

    Attributes:
        source (DirectoryPath): Path to the source folder.
        replica (DirectoryPath): Path to the replica folder.
        interval (Annotated[int, Field(gt=0)]): Synchronization interval in seconds (must be > 0).
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
    replica: Path = Field(default=Path(os.getcwd(), "output", "replica"))
    interval: Annotated[int, Field(gt=0)] = 60
    log_file: Path = Field(default=Path(os.getcwd(), "output", "logfile.log"))

    @model_validator(mode="before")
    def check_and_create__directories(cls, values: dict) -> dict:  # noqa: N805
        """
        Prevalidate before model is fully initialized.
        Permission update for 'source' and 'replica' folders.

        Args:
            cls (self): The class itself (used by Pydantic for validation).
            values (dict): A dictionary of field names and values.

        Returns:
            dict: The same dictionary of values after validation, with potential
                  side effects of creating the log file's parent directory.

        Raises:
            ValueError: If `log_file` is not specified in the `values` dictionary.
        """
        log_file_path = values.get("log_file")
        source = values.get("source")
        replica = values.get("replica")

        # Check if source directory exists
        if not source or not Path(source).exists():
            raise ValueError(f"The source directory '{source}' does not exist.")

        source = Path(source)
        if not source.is_absolute():
            raise ValueError(f"The path '{source}' is not a full path.")

        # Validate replica directory
        if not replica:
            replica = Path(os.getcwd(), "output", "replica")
            values["replica"] = replica
        else:
            replica = Path(replica)

        if not replica.is_absolute():
            raise ValueError(f"The path '{replica}' is not a full path.")

        # Ensure the parent directory of the log file exists
        if not log_file_path:
            log_file_path = Path(os.getcwd(), "output", "logfile.log")
            values["log_file"] = log_file_path
        log_file_path = Path(log_file_path)

        if not log_file_path.is_absolute():
            raise ValueError(f"The path '{replica}' is not a full path.")

        if not Path(log_file_path).exists():
            # folder creation needed for logging
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

        return values

    @staticmethod
    def update_permissions(path: Path):
        """
        Update permissions of the given directory to ensure read and write access.

        Args:
            path (Path): Path to the directory or file.

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


@lru_cache
def arguments_parser() -> ArgumentsModel:
    """
    Uses `argparse` for argument parsing and `pydantic` for validation.
    
    Does the following:
        - parse command-line arguments
        - validate them against the `ArgumentsModel` model
        - return the validated arguments as a dictionary.
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

    return args_model
