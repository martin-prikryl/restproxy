'''
now API
'''
from datetime import datetime
from flask_restful import Resource


class Now(Resource):

    @staticmethod
    def get():
        now: str = datetime.now().isoformat(timespec='seconds')
        return {'now': now}
