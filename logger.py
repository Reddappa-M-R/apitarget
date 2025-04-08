import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("vercel_app")
logger.setLevel(LOG_LEVEL)

# Remove existing handlers if reloading
if logger.hasHandlers():
    logger.handlers.clear()

# ✅ StreamHandler logs to console (safe for Vercel)
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
