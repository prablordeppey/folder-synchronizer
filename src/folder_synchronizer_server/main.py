from datetime import datetime
from typing import Dict, Union

import uvicorn
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.utils import setup_parent_dirs
from core.cli import ArgumentsModel, arguments_parser
from core.logger import MainLogger
from core.synchronizer import FolderSynchronizer
from folder_synchronizer_server.log_config import log_config

# Grab cli arguments instantiate logger
args_model = arguments_parser()
logger = MainLogger("server_main", log_file=args_model.log_file, overwrite=True)

app = FastAPI()
scheduler = BackgroundScheduler()
sync_count = 0


def scheduled_sync():
    """
    Executes the synchronization task using the current configuration in `args_model`.

    This function initializes the `FolderSynchronizer` with the global logger and
    performs the synchronization between the source and replica folders as specified
    in `args_model`.

    - Uses the `FolderSynchronizer` class to handle the synchronization logic.
    - Accesses global `args_model` to get the source and replica paths.
    - Logs messages according to the configured logging settings.
    """
    global args_model
    global sync_count

    sync_count += 1

    # Initialize the folder synchronizer with the global logger
    folder_synchronizer = FolderSynchronizer(logger=logger)

    # Perform synchronization between source and replica directories
    folder_synchronizer.sync_folders(args_model.source, args_model.replica)


@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event handler to initialize background tasks.

    This function is triggered when the FastAPI application starts up. It configures
    and starts a background job that synchronizes folders at the interval specified
    in the global `args_model`. The job is scheduled to start immediately.

    The job's schedule and parameters can be updated via the `/update_sync_params/` endpoint.

    - Adds a job to the APScheduler to run the `scheduled_sync` function.
    - Uses an `IntervalTrigger` with the interval specified in `args_model`.
    - Sets the job to start immediately upon application startup.
    """
    global args_model

    # Remove any existing job with the same ID
    if scheduler.get_job("sync_job"):
        scheduler.remove_job("sync_job")

    # Add or update the job with the new interval
    scheduler.add_job(
        scheduled_sync,
        IntervalTrigger(seconds=args_model.interval),
        id="sync_job",
        name=f"Synchronize folders every {args_model.interval} seconds.",
        replace_existing=True,
        next_run_time=datetime.now(),  # Schedule to start immediately
    )
    scheduler.start()


@app.get("/", summary="Retrieve synchronization count and CLI arguments")
def root():
    """
    Retrieve the current synchronization status and command-line arguments.

    Provides information about the current number of synchronizations
    and the parameters provided via the command-line interface.

    **Responses:**
    
    - **200 OK**: Returns the current synchronization count and the command-line arguments.
    - **500 Internal Server Error**: If an error occurs while retrieving the synchronization status.

    Returns:
        Union[str, int]: A dictionary with the keys `Sync Count` and `CLI Args`.
    """
    return {"Sync Count": sync_count, "CLI Args": args_model}


@app.get("/get_sync_params/", response_model=ArgumentsModel)
def get_sync_params() -> Union[str, int]:
    """
    Retrieve the current synchronization parameters.

    This endpoint returns the current settings for synchronization, including

    - the source folder path
    - replica folder path
    - synchronization interval
    - log file path

    Returns:
        ArgumentsModel: The current synchronization parameters.

    Example Response:
        {
            "source": "path/to/source",
            "replica": "path/to/replica",
            "interval": 60,
            "log_file": "path/to/logfile.log"
        }
    """
    global args_model
    return args_model


@app.post("/update_sync_params/")
def update_sync_params(args: ArgumentsModel) -> Dict:
    """
    Update synchronization parameters and reschedule the synchronization job.

    This endpoint updates the synchronization parameters (source, replica, interval,
    log_file) and reschedules the synchronization job with the new interval.

    Args:
        args (ArgumentsModel): The new synchronization parameters.

    Returns:
        dict: A message indicating that the synchronization parameters were updated.

    Raises:
        HTTPException: If the scheduler is not running.
    """
    global args_model
    args_model = args

    if not scheduler.running:
        raise HTTPException(status_code=500, detail="Scheduler is not running.")

    # Remove the existing job and add a new one with updated parameters
    scheduler.remove_job("sync_job")
    scheduler.add_job(
        scheduled_sync,
        IntervalTrigger(seconds=args_model.interval),
        id="sync_job",
        name=f"Synchronize folders at ({args_model.interval} secs) intervals.",
        replace_existing=True,
        next_run_time=datetime.now(),  # Schedule to start immediately
    )
    return {"message": "Synchronization parameters updated"}


if __name__ == "__main__":
    source = args_model.source
    replica = args_model.replica
    log_file = args_model.log_file
    INTERVAL = args_model.interval

    # Instantiate the logger
    logger.info(f"Parsed arguments:  {args_model}")

    # Setup parent directories
    logger.info("Setting-up parent directories ...")
    setup_parent_dirs(args_model, logger)

    logger.info(f"Starting synchronization: {source} -> {replica} every {INTERVAL} seconds")

    # Dynamically update the log file name in the log configuration.
    log_config()["handlers"].update(
        {
            "logfile": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": log_file,
                "mode": "a",
                "maxBytes": 1048576,
            }
        }
    )
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config())
