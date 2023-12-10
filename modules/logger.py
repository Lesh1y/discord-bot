from logging import Formatter, getLogger
from logging.handlers import TimedRotatingFileHandler

from modules.conf import LOG_FILENAME, LOG_LEVEL

_format = Formatter('%(asctime)-25s %(module)-25s %(levelname)-10s %(message)s')

handler = TimedRotatingFileHandler(LOG_FILENAME, encoding='utf-8', when='D')
handler.setLevel(LOG_LEVEL)
handler.setFormatter(_format)
handler.suffix = "%d-%m-%Y"

logger = getLogger('qwerty_bot')
logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)
