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
        # start request threads
        self._start_request_threads(point_in_time)

        # wait for response
        while not self.response_json and self._request_threads_running():
            sleep(0.05)

        # check response
        try:
            latitude = self.response_json['latitude']
            longitude = self.response_json['longitude']
        # TypeError in case of None, KeyError in case of missing key
        except (TypeError, KeyError):
            return self._internal_error()
        return self._success_response(latitude, longitude)

    @staticmethod
    def _internal_error():
        return {'message': 'Internal Server Error'}, 500

    @staticmethod
    def _success_response(latitude: str, longitude: str):
        return {
            'source': 'vip-db',
            'gpsCoords': {'lat': latitude, 'long': longitude}}, 200

    def _start_request_threads(self, point_in_time):
        # check request threads exist
        if self.request_threads:
            # only log error, don't fail
            self.logger.error('Seems to be attempt to start request threads for second time.')
            return

        # create and start request threads
        vip_db_api_url = urllib.parse.urljoin(config.VIP_DB_API, str(point_in_time))
        for _ in range(config.REQUEST_THREADS):
            thread = Thread(target=self._request_json, args=(vip_db_api_url,))
            self.request_threads.append(thread)
            thread.start()

    def _request_threads_running(self) -> bool:
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

    def _request_json(self, vip_db_api_url: str):
        ''' method to be executed by request thread '''
        print(vip_db_api_url)
        try:
            response = requests.get(vip_db_api_url, timeout=config.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return
        if response.status_code == 200:
            self.response_json = response.json()
