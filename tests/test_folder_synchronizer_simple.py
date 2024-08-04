import unittest
import filecmp
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil
import os
import pytest

from core.cli import ArgumentsModel
from core.logger import MainLogger
from core.synchronizer import FolderSynchronizer


class TestFolderSynchronizerSimple(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Define paths for the test
        cls.root_folder = Path(os.getcwd(), "tests", "resources")
        cls.source_path = Path(cls.root_folder, "source")

        output_path = Path(cls.root_folder, "output")
        cls.replica_path = Path(output_path, "replica")
        cls.log_file_path = Path(output_path, "logfile.log")

    def setUp(self):
        # Create source resource
        os.makedirs(self.source_path, exist_ok=True)
        os.makedirs(self.replica_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.source_path, ignore_errors=True)
        shutil.rmtree(self.replica_path, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root_folder, ignore_errors=True)

    def is_dirs_identical(self, source_path: str, replica_path: str):
        """
        Recursively compare two directories to check if they are identical.

        This method compares two directories and their contents recursively
        to determine if they are identical. It checks for the presence of
        files and directories, as well as the contents of files.

        Args:
            source_path (str): Path to the source directory.
            replica_path (str): Path to the replica directory.

        Returns:
            bool: True if both dirs are identical
        """
        dir_comparison = filecmp.dircmp(source_path, replica_path)

        # Check if there are any files or directories only in one of the directories.
        if dir_comparison.left_only or dir_comparison.right_only or dir_comparison.funny_files:
            return False

        # Compare files in both directories.
        _, mismatch, errors = filecmp.cmpfiles(source_path, replica_path, dir_comparison.common_files, shallow=False)
        if mismatch or errors:
            return False

        # Recursively compare subdirectories.
        for common_dir in dir_comparison.common_dirs:
            new_source_path = os.path.join(source_path, common_dir)
            new_replica_path = os.path.join(replica_path, common_dir)
            if not self.is_dirs_identical(new_source_path, new_replica_path):
                return False

        return True

    def test_sync_folders_end2end_source_w_files(self):
        """Source with only files."""
        # Prepare
        Path(self.source_path, "file1.txt").write_text("This is a test file.", encoding="utf8")
        Path(self.source_path, "file2.txt").write_text("This is another test file.", encoding="utf8")

        args_model = ArgumentsModel(
            source=self.source_path,
            replica=self.replica_path,
        )

        # Act
        synchronizer = FolderSynchronizer()
        synchronizer.sync_folders(args_model.source, args_model.replica)

        # Assert
        assert self.is_dirs_identical(self.source_path, self.replica_path)

    def test_sync_folders_end2end_source_w_subdirs(self):
        """Source with subdirs"""
        # Prepare
        Path(self.source_path, "subdir1").mkdir(parents=True, exist_ok=True)
        Path(self.source_path, "subdir2").mkdir(parents=True, exist_ok=True)
        Path(self.source_path, "subdir1", "subsubdir1").mkdir(parents=True, exist_ok=True)
        Path(self.source_path, "subdir2", "subsubdir2", "subsubsubdir1").mkdir(parents=True, exist_ok=True)

        args_model = ArgumentsModel(
            source=self.source_path,
            replica=self.replica_path,
        )

        # Act
        synchronizer = FolderSynchronizer()
        synchronizer.sync_folders(args_model.source, args_model.replica)

        # Assert
        assert self.is_dirs_identical(self.source_path, self.replica_path)

    def test_sync_folders_end2end_source_w_subdirs_n_files(self):
        """Source with subdirs and files. Replicate for replica"""
        # Prepare
        Path(self.source_path, "file1.txt").write_text("This is a test file.", encoding="utf8")
        Path(self.source_path, "subdir1", "subdir2").mkdir(parents=True, exist_ok=True)
        Path(self.source_path, "subdir1", "subdir2", "file2.txt").write_text("This is a test file.", encoding="utf8")

        args_model = ArgumentsModel(
            source=self.source_path,
            replica=self.replica_path,
        )

        # Act
        synchronizer = FolderSynchronizer()
        synchronizer.sync_folders(args_model.source, args_model.replica)

        # Assert
        assert self.is_dirs_identical(self.source_path, self.replica_path)

    def test_sync_folders_end2end_w_replica_subdir(self):
        """replica with additional files than source. Truncate replica"""
        # Prepare
        Path(self.source_path, "file1.txt").write_text("This is a test file.", encoding="utf8")
        Path(self.replica_path, "file1.txt").write_text("This is a test file.", encoding="utf8")

        Path(self.replica_path, "file3.txt").write_text("This is another test file1.", encoding="utf8")
        Path(self.replica_path, "dir3").mkdir(parents=True, exist_ok=True)
        Path(self.replica_path, "dir3", "file3.txt").write_text("This is another test file1.", encoding="utf8")

        args_model = ArgumentsModel(
            source=self.source_path,
            replica=self.replica_path,
        )

        # Act
        synchronizer = FolderSynchronizer()
        synchronizer.sync_folders(args_model.source, args_model.replica)

        # Assert
        assert self.is_dirs_identical(self.source_path, self.replica_path)
