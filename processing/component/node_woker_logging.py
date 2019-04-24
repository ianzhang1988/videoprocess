# coding=utf-8
from ..core.pipe_node import PipeNode
from ..processing_exception import *
import logging, logging.handlers, os

class WorkerLogging(PipeNode):
    def __init__(self):
        super(WorkerLogging, self).__init__()

    def init(self):
        try:
            video_id = self.params['video_id']
            work_dir = self.params['work_dir']

            log_file = '%s.log' % video_id

            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

            fh = logging.FileHandler(os.path.join(work_dir, log_file))
            #fh = logging.handlers.TimedRotatingFileHandler(os.path.join(work_dir, log_file), when='D', backupCount=7)
            formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
            fh.setFormatter(formatter)

            logger.addHandler(fh)

        except Exception as e:
            import traceback
            logging.error('set logging error: %s', traceback.format_exc())
            self.error(ERROR_INTERNAL_ERROR, 'set logging error: %s' % str(e))
            return False

        return True
