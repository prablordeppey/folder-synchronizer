from functools import lru_cache


@lru_cache
def log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "logfile": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logfile.log",
                "mode": "a",
                "maxBytes": 1048576,
                "backupCount": 3,
            },
            "logconsole": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["logfile", "logconsole"],
        },
    }
