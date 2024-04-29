from logging import basicConfig, DEBUG, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from os import makedirs

from modules.conf import LOG_FILE_LEVEL, LOG_FILE_PATH, LOG_STREAM_LEVEL, LOGS_DIR
from qwerty_bot import QwertyBot

if __name__ == '__main__':
    makedirs(LOGS_DIR, exist_ok=True)

    time_handler = TimedRotatingFileHandler(LOG_FILE_PATH, encoding='utf-8', when='D')
    time_handler.suffix = "%d-%m-%Y"
    time_handler.setLevel(LOG_FILE_LEVEL)

    stream_handler = StreamHandler()
    stream_handler.setLevel(LOG_STREAM_LEVEL)

    basicConfig(
        format='%(asctime)-25s %(module)-25s %(levelname)-10s %(message)s',
        encoding='utf-8',
        level=DEBUG,
        handlers=(time_handler, stream_handler),
        force=True
    )

    QwertyBot().startup()
