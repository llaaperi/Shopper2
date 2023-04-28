import logging

# Levels
CRITICAL = logging.CRITICAL #50
ERROR = logging.ERROR       #40
WARNING = logging.WARNING   #30
INFO = logging.INFO         #20
DEBUG = logging.DEBUG       #10
NOTSET = logging.NOTSET     #0

# Format
FORMAT = '%(asctime)s %(levelname)s %(name)s(%(lineno)d):%(message)s'

logging.basicConfig(format=FORMAT, level=WARNING)

def get(name, level=INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
