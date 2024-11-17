import logging
import logging.config

logging.config.fileConfig('logging.conf',disable_existing_loggers=False)

# create file handler which logs even debug messages
#fh = logging.FileHandler('logging2.log')

# create logger
logger = logging.getLogger('main')

# add the handlers to logger
#logger.addHandler(fh)

# 'application' code
def log_debug(string:str):
    logger.debug(string)

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')