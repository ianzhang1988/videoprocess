#coding=utf-8

import requests
import logging
import json
import threading

class AsyncReport():
    def __init__(self):
        self.report_url = 'http://10.18.113.31:9090/glue/transcodingFailed'

    def post(self, data):
        try:
            data = json.dumps(data)
            response = requests.post(self.report_url,data=data,headers={'Connection':'close'}, timeout=5)
            response.raise_for_status()
        except Exception as e:
            logging.error('FaceReport: %s' % str(e))
            return False

    def error(self, video_id, code, msg):
        t = threading.Thread(target=self._error, args=(video_id, code, msg))
        t.start()

    def _error(self, video_id, code, msg):
        report = {
            'video_id': video_id,
            'status': 'error',
            'error_type': code,
            'info': msg,
        }

        self.post(report)

if __name__ == '__main__':
    import time
    r = AsyncReport()
    r.error('1000',1,'test')
    time.sleep(2)


