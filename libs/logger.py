import logging
from logging.handlers import TimedRotatingFileHandler

from config import logFormat, logDateFormat, logLevel, logFile

formatter = logging.Formatter(fmt=logFormat, datefmt=logDateFormat)

logger = logging.getLogger()
logger.setLevel(logLevel)

time_handler = TimedRotatingFileHandler(filename=logFile, when='D', interval=1, backupCount=7)
time_handler.setLevel(logLevel)
time_handler.setFormatter(formatter)
logger.addHandler(time_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
