import logging

logging.basicConfig(format='%(asctime)s - %(name)s :: %(funcName)20s() - [%(levelname)s] - %(message)s',
                    level=logging.INFO)
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s - %(name)s :: %(funcName)20s() - [%(levelname)s] - %(message)s')
# logging_handler = logging.NullHandler()
# logging_handler.setFormatter(formatter)
# logger.addHandler(logging_handler)
# logger.setLevel(logging.INFO)
