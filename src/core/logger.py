import logging
from logging.handlers import RotatingFileHandler

from core.settings import BASE_PATH

logger_path = BASE_PATH / "logs" / "logs.log"
logger_path.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("vpn_bot")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    filename=logger_path, maxBytes=1 * 1024 * 1024, backupCount=0, encoding="utf-8"
)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(stream_handler)
