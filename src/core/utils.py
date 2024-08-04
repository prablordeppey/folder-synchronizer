from core.cli import ArgumentsModel
from core.logger import MainLogger


def setup_parent_dirs(cli_arguments: ArgumentsModel, logger: MainLogger):
    """
    Ensure the parent directories for the replica directory exist and set permissions for source and replica.

    Args:
        cli_arguments (ArgumentsModel): The arguments model containing source and replica paths.
        logger (MainLogger): Logger instance to record debug information.

    Steps:
        - Creates parent directories for the replica if they do not exist.
        - Updates read/write permissions for both source and replica directories.
    """
    source = cli_arguments.source
    replica = cli_arguments.replica

    # Create parent directories for replica if they do not exist
    if not replica.exists():
        logger.debug("Creating parent directories for replica.")
        replica.mkdir(parents=True, exist_ok=True)

    # Update permissions for source and replica directories
    logger.debug("Updating read/write permissions for source.")
    cli_arguments.update_permissions(source)

    logger.debug("Updating read/write permissions for replica.")
    cli_arguments.update_permissions(replica)
