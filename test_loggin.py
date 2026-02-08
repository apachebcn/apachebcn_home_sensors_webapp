import logging

logger = logging.getLogger('django')

def log_test_messages():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

log_test_messages()

