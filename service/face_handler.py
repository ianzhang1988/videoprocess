# coding=utf-8

import tornado.web
import json
from .async_report import AsyncReport

ERROR_POOL_FULL = 101

class FaceHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.work_pool = self.application.work_pool
        pass

    def post(self):
        data = self.request.body
        params = json.loads(data)

        # params['video_id']
        # params['pic_url']
        # params['template_id']

        succeed = self.work_pool.add_job(params)
        if not succeed:
            report_error = AsyncReport()
            video_id = 'unknow'
            if 'video_id' in params:
                video_id = params['video_id']

            report_error.error(video_id,ERROR_POOL_FULL,'pool full')



