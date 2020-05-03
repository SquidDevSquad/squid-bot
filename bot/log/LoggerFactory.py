import logging

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s :: %(funcName)20s() - [%(levelname)s] - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
