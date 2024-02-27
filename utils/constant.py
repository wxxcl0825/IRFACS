import logging

from view.logs import LoggingHandler

# paths
PATH_WORK_DIR = "D:/Dataset/IRpic/work"
PATH_TEMPLATE_DIR = "D:/Dataset/IRpic/template"
PATH_DB = 'D:/Dataset/IRpic/data.db'
PATH_MODEL = 'D:/Dataset/IRpic/model.pkl'
PATH_SAVE = 'D:/Dataset/IRpic/save'
PATH_WAV = "temp/temp.wav"
PATH_MP3 = "temp/temp.mp3"

# network addr
PATH_PI_ADDR = ("10.189.36.109", 6666)

MESSAGE = "你好,{}"
MAX_RETRY = 5

LOGGER = logging.Logger("logger")
LOGGER.addHandler(LoggingHandler(None))
