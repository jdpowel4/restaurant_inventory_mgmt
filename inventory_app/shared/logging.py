import logging
from logging.handlers import RotatingFileHandler
import functools
import time

from inventory_app.shared.config import LOG_DIR, LOG_LEVEL

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "inventory_app.log"

class LogLevels():
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10


def setup_logging() -> logging.Logger:

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("inventory_app")

    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)-60s | %(funcName)-25s | %(message)s",
        datefmt="%y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10_000_000,
        backupCount=5
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
"""
def log_operation(func, level: int = logging.DEBUG):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
            
        logger = logging.getLogger(func.__name__)
            
        start = time.perf_counter()

        logger.log(
            level,
            f"Entering {func.__qualname__}()"
        )

        try:
            return func(*args, **kwargs)

        finally:
            elapsed = time.perf_counter() - start

            logger.log(
                level,
                f"Leaving {func.__qualname__}()"
                f"({elapsed:.3f}s)"
            )

    return wrapper
"""
def log_operation(func=None, *, level: int = logging.DEBUG):

    def decorator(f):
    
        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            logger = logging.getLogger(f.__module__)

            start = time.perf_counter()

            logger.log(
                level,
                f"Starting {f.__qualname__}",
                stacklevel=2)

            try:
                return f(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start

                logger.log(
                    level,
                    f"Finished {f.__qualname__} in {elapsed:.4f}s",
                    stacklevel=2)

        return wrapper
    
    if func is None:
        return decorator
    
    return decorator(func)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)