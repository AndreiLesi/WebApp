from logging.handlers import RotatingFileHandler
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s: %(message)s')
file_handler = RotatingFileHandler('TrueTest.log', mode="w")
file_handler.doRollover()
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main():
    logger.info(f"-------------Started test: {__name__}-------------")
    logger.info("Test passed")
    assert True


if "__name__" == "__main__":
    main()
