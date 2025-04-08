### logger.py
import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL

logger = logging.getLogger("vercel_app")
logger.setLevel(LOG_LEVEL)

if logger.hasHandlers():
    logger.handlers.clear()

# Console handler (stdout)
console_handler = logging.StreamHandler()
console_format = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File logging for local only
if os.environ.get("VERCEL") != "1":
    file_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(console_format)
    logger.addHandler(file_handler)