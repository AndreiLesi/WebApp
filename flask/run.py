from tester_webapp import app
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s: %(message)s')
# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
# logger.addHandler(file_handler)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
