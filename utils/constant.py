import logging

from view.logs import LoggingHandler

# paths
PATH_WORK_DIR = None
PATH_TEMPLATE_DIR = None
PATH_DB = None
PATH_MODEL = None
PATH_SAVE = None
PATH_WAV = None
PATH_MP3 = None

# network addr
PATH_PI_ADDR = ("0.0.0.0", 6666)

MESSAGE = "你好,{}"
MAX_RETRY = 5

LOGGER = logging.Logger("logger")
LOGGER.addHandler(LoggingHandler())
