import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FILE

logger = logging.getLogger("app_logger")
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

# Rotating file handler
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console (for Vercel or local dev)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
