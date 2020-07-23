import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s: %(message)s')

file_handler = RotatingFileHandler('FalseTest.log', mode="w")
file_handler.setFormatter(formatter)
file_handler.doRollover()

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main():
    logger.info(f"-------------Started test: {__name__}-------------")
    logger.warning("Test Failed!")
    assert False


if __name__ == "__main__":
    main()
