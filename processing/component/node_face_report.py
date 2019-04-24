#coding=utf-8

from ..core.pipe_node import PipeNode
from ..processing_exception import *
import requests
import logging
import json

class FaceReport(PipeNode):
    def __init__(self):
        super(FaceReport, self).__init__()
        #self.report_url = 'http://10.18.113.31:9090/glue/transcodingFailed'
        self.report_url = 'http://qipai.56.com/camera/glue/transcodingFailed'

    def post(self, data):
        try:
            data = json.dumps(data)
            response = requests.post(self.report_url,data=data,headers={'Connection':'close'}, timeout=5)
            response.raise_for_status()
        except Exception as e:
            logging.error('FaceReport: %s' % str(e))
            return False

    def do(self):

        video_id = self.params['video_id']
        if 'error' in self.params:
            code = self.params['error']['code']
            msg = self.params['error']['msg']

            report = {
                'video_id': video_id,
                'status':'error',
                'error_type': code,
                'info': msg,
            }

            self.post(report)

        else:
            report = {
                'video_id': video_id,
                'status': 'ok'
            }

            self.post(report)


