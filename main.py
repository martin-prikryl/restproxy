'''
Implementation of REST API proxy
'''

import logging
import sys

from flask import Flask
from flask_restful import Api

import config
from now import Now
from vip import VIP


def init_logger():
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stdout_handler)


if __name__ == '__main__':
    init_logger()

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Now, '/v1/now')
    api.add_resource(VIP, '/v1/VIP/<int:point_in_time>')

    app.run()
