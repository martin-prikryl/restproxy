'''
VIP API
'''
import logging
import urllib
from threading import Thread
from time import sleep
from typing import List

import requests
from flask_restful import Resource

import config


class VIP(Resource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.request_threads: List[Thread] = []
        self.response_json = None
        self.logger = logging.getLogger(config.LOGGER_NAME)

    def get(self, point_in_time):
        self.logger.info(point_in_time)
        # start request threads
        self._start_request_threads(point_in_time)

        # wait for response
        while not self.response_json and self._request_threads_running():
            sleep(0.05)

        # check response
        if self.response_json:
            try:
                return {
                    'source': 'vip-db',
                    'gpsCoords': {
                        'lat': self.response_json['latitude'],
                        'long': self.response_json['longitude']}}
            except KeyError:
                return self._internal_error()
        return self._internal_error()

    @staticmethod
    def _internal_error():
        return {'message': 'Internal Server Error'}, 500

    def _start_request_threads(self, point_in_time):
        # check request threads exist
        if self.request_threads:
            # only log error, don't fail
            self.logger.error('Seems to be attempt to start request threads for second time.')
            return

        # create and start request threads
        for _ in range(config.REQUEST_THREADS):
            thread = Thread(target=self._request_json, args=(point_in_time,))
            self.request_threads.append(thread)
            thread.start()

    def _request_threads_running(self):
        # check request threads exists
        if not self.request_threads:
            self.logger.error('Seems to be attempt to check request threads'
                              ' status before starting them.')
            return False

        # try to find at least one running request thread
        for thread in self.request_threads:
            if thread.is_alive():
                return True
        return False

    def _request_json(self, point_in_time):
        ''' request thread function '''
        vip_db_api_url = urllib.parse.urljoin(config.VIP_DB_API, str(point_in_time))
        try:
            response = requests.get(f'{vip_db_api_url}', timeout=config.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return
        if response.status_code == 200:
            self.response_json = response.json()
