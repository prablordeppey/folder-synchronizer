import shutil
import unittest
import logging
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
from core.logger import MainLogger

class TestMainLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_folder = Path(os.getcwd(), "tests", "resources")
        cls.output_folder = Path(os.getcwd(), "output")
        cls.log_file_path = cls.root_folder / "test_log.log"

    def setUp(self):
        # Set up mock for logger
        self.mock_logger = MagicMock()
        self.mock_stream_handler = MagicMock()
        self.mock_file_handler = MagicMock()

    def tearDown(self):
        # Clean up log file if it exists
        if self.log_file_path.exists():
            # self.log_file_path.unlink(missing_ok=True)  # PermissionError file locked by another process
            shutil.rmtree(self.log_file_path, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root_folder, ignore_errors=True)

        if cls.output_folder.exists():
            shutil.rmtree(cls.output_folder)

    @patch("logging.getLogger")
    def test_console_logging(self, mock_get_logger):
        """Logging to console"""
        # Prepare
        mock_get_logger.return_value = self.mock_logger

        # Act
        logger = MainLogger(name="test_logger")
        logger.info("This is an info message.")
        logger.error("This is an error message.")
        logger.debug("This is a debug message.")

        # Assert
        self.mock_logger.info.assert_any_call("This is an info message.")
        self.mock_logger.error.assert_any_call("This is an error message.")
        self.mock_logger.debug.assert_any_call("This is a debug message.")
        self.mock_logger.info.assert_any_call("\n" + "-" * 50)
        self.mock_logger.info.assert_any_call("Starting new logging session")
        self.mock_logger.info.assert_any_call("No log file specified; logging to console only.")

    @patch("logging.getLogger")
    def test_file_logging(self, mock_get_logger):
        """Logging to overwrite to file."""
        mock_get_logger.return_value = self.mock_logger

        logger = MainLogger(name="test_logger", log_file=self.log_file_path, overwrite=True)

        logger.info("This is an info message.")
        logger.error("This is an error message.")
        logger.debug("This is a debug message.")

        self.mock_logger.info.assert_any_call("This is an info message.")
        self.mock_logger.error.assert_any_call("This is an error message.")
        self.mock_logger.debug.assert_any_call("This is a debug message.")
        self.mock_logger.info.assert_any_call("\n" + "-" * 50)
        self.mock_logger.info.assert_any_call("Starting new logging session")
        self.mock_logger.info.assert_any_call(f"Log file: {self.log_file_path}")
        self.mock_logger.info.assert_any_call("Overwrite mode: Yes")

    @patch("logging.getLogger")
    def test_append_file_logging(self, mock_get_logger):
        """Logging to append to file"""
        # Prepare
        mock_get_logger.return_value = self.mock_logger
        os.makedirs(self.log_file_path.parent, exist_ok=True)
        with open(self.log_file_path, "w", encoding="utf8") as f:
            f.write("Initial log entry.\n")

        # Act
        logger = MainLogger(name="test_logger", log_file=self.log_file_path, overwrite=False)
        logger.info("This is an appended info message.")

        # Assert
        self.mock_logger.info.assert_any_call("This is an appended info message.")
        self.mock_logger.info.assert_any_call("\n" + "-" * 50)
        self.mock_logger.info.assert_any_call("Starting new logging session")
        self.mock_logger.info.assert_any_call(f"Log file: {self.log_file_path}")
        self.mock_logger.info.assert_any_call("Overwrite mode: No")

    @patch("logging.getLogger")
    def test_log_levels(self, mock_get_logger):
        """Logging specific levels."""
        mock_get_logger.return_value = self.mock_logger

        logger = MainLogger(name="test_logger", log_level=logging.DEBUG)

        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.error("This is an error message.")

        self.mock_logger.debug.assert_any_call("This is a debug message.")
        self.mock_logger.info.assert_any_call("This is an info message.")
        self.mock_logger.error.assert_any_call("This is an error message.")
