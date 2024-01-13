import logging
import os
from logging.handlers import RotatingFileHandler

# Remove Old Log File
try:
    os.remove("logs.txt")
except BaseException:
    pass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt",
            maxBytes=5000000,
            backupCount=10,
            encoding="utf8",
        ),
        logging.StreamHandler(),
    ],
)

LOG = logging.getLogger("pyrogram").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)