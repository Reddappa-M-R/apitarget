import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FILE

logger = logging.getLogger("vercel_app")
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Only use file logging locally or if write permissions are available
if os.environ.get("ENV") != "vercel":
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
