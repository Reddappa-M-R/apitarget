import os
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL

logger = logging.getLogger("vercel_app")
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")

# Stream handler (for Vercel logs / console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# File handler (only for local)
if os.environ.get("ENV") != "vercel":
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, "log.log"), maxBytes=1000000, backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
