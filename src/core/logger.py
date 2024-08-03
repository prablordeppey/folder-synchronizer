import logging
from pathlib import Path
from typing import Optional


class MainLogger:
    """
    A logging utility class to handle logging configuration and usage.
    This class sets up a logger with console and optional file handlers.

    Attributes:
        logger (logging.Logger): The logger instance for this class.
        overwrite (bool): If True, the log file will be overwritten each time.
            If False, logs will be appended. Defaults to False.
    """

    def __init__(
        self, name: str, log_file: Optional[Path] = None, log_level: int = logging.INFO, overwrite: bool = False
    ) -> None:
        """
        Initialize the MainLogger with the specified module name and optional file logging.

        Args:
            name (str): The name of the module or application using the logger.
            log_file (Optional[Path], optional): The path to the log file. If not provided,
                logging will be only to the console. Defaults to None.
            log_level (int, optional): The logging level to set for the logger and handlers. Defaults to logging.INFO.
            overwrite (bool, optional): If True, the log file will be overwritten each time the logger is initialized.
                If False, logs will be appended to the file. Defaults to False.

        Raises:
            ValueError: If `log_level` is not a valid logging level.

        Example:
            >>> logger = MainLogger(
                    name="my_module",
                    log_file=Path("/path/to/logfile.log"),
                    log_level=logging.DEBUG, overwrite=True
                )
            >>> logger.logger.info("This is an info message.")
            >>> logger.logger.error("This is an error message.")
        """
        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Create console handler and set level to info
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Create file handler if log_file is provided
        if log_file:
            file_mode = "w" if overwrite else "a"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file, mode=file_mode)
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        # Update user with important metrics and start new logging session
        self._log_start_of_session(log_file, overwrite)

    def _log_start_of_session(self, log_file: Optional[Path], overwrite: bool) -> None:
        self.logger.info("\n" + "-" * 50)
        self.logger.info("Starting new logging session")
        if log_file:
            self.logger.info(f"Log file: {log_file}")
            self.logger.info(f"Overwrite mode: {'Yes' if overwrite else 'No'}")
        else:
            self.logger.info("No log file specified; logging to console only.")

    def info(self, message: str):
        """
        Log an info level message.

        Args:
            message (str): The message to be logged.
        """
        self.logger.info(message)

    def error(self, message: str):
        """
        Log an error level message.

        Args:
            message (str): The message to be logged.
        """
        self.logger.error(message)

    def debug(self, message: str):
        """
        Log a debug level message.

        Args:
            message (str): The message to be logged.
        """
        self.logger.debug(message)
