import unittest
import os
import stat
import shutil
import pytest
from unittest.mock import patch, call
from pathlib import Path

from pydantic import ValidationError

from core.cli import ArgumentsModel  # Replace with actual import path


class TestArgumentsModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_root = Path(os.getcwd(), "tests", "resources")
        cls.source_path = cls.test_root / "source"
        cls.replica_path = cls.test_root / "replica"
        cls.log_file_path = cls.test_root / "output" / "logfile.log"
        cls.source_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if cls.test_root.exists():
            shutil.rmtree(cls.test_root)

        if cls.test_root.exists():
            shutil.rmtree(Path(os.getcwd(), "output"))

    def test_valid_arguments(self):
        args = ArgumentsModel(
            source=self.source_path, replica=self.replica_path, interval=60, log_file=self.log_file_path
        )
        self.assertEqual(args.source, self.source_path)
        self.assertEqual(args.replica, self.replica_path)
        self.assertEqual(args.interval, 60)
        self.assertEqual(args.log_file, self.log_file_path)

    def test_default_replica_and_log_file(self):
        """When no log_file is given, assert default generation"""
        # Prepare
        self.test_root = Path(os.getcwd()) / "output"
        expected_replica_path = self.test_root / "replica"
        expected_log_file_path = self.test_root / "logfile.log"

        # Act
        args = ArgumentsModel(source=self.source_path)

        # Assert
        self.assertEqual(args.replica, expected_replica_path)
        self.assertEqual(args.log_file, expected_log_file_path)

    def test_update_permissions(self):
        """Read/Write permissions for files and dirs"""
        # Act
        args = ArgumentsModel(source=self.source_path, replica=self.replica_path)

        # Assert
        # Check permissions for source and replica directories
        for path in [self.source_path, self.replica_path]:
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    self.assertTrue(os.access(dir_path, os.R_OK | os.W_OK | os.X_OK))
                for f in files:
                    file_path = os.path.join(root, f)
                    self.assertTrue(os.access(file_path, os.R_OK | os.W_OK))


# VALIDATION CHECKS
class TestArgumentsModelValidation:
    """For cli args validation"""

    @pytest.mark.parametrize(
        "cli_vars,error_type",
        [
            # TestCase1: source not existing dir
            ({"source": Path("/non/existent/source")}, ValidationError),

            # TestCase2: replica not existing dir
            ({"replica": Path("/non/existent/replica")}, ValidationError),

            # TestCase3: log_file not existing dir
            ({"log_file": Path("/non/existent/logfile.log")}, ValidationError),

            # TestCase4: interval not a vaid positive
            ({"interval": -1}, ValidationError),
        ],
        ids=["TestCase1", "TestCase2", "TestCase3", "TestCase4"],
    )
    def test_invalid_paths(self, cli_vars: dict, error_type: Exception):
        """Given dir paths do not exist"""

        # Act, Assert
        with pytest.raises(error_type):
            ArgumentsModel(**cli_vars)
