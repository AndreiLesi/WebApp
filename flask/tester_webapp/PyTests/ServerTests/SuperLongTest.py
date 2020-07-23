import random
import time
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s: %(message)s')
file_handler = RotatingFileHandler('SuperLongTest.log', mode="w")
file_handler.doRollover()
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main():
    '''Generate a random Short Test, where the test duration is at maximum 10
    seconds and the result is either True or False'''
    Duration = random.randint(30, 40)
    Result = random.randint(0, 100)

    logger.info(f"-------------Started test: {__name__}-------------")
    time.sleep(Duration)

    try:
        assert Result >= 50, "Test failed !!!"
    except AssertionError as error:
        logger.warning(error)
        raise error

    logger.info("Test passed")
    assert True


# Run Test
if __name__ == '__main__':
    main()
