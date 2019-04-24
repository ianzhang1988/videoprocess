# coding=utf-8

import logging
from ..processing_exception import *

class SubPipe():
    class Finish():
        pass
    def __init__(self):
        self.pipe = None
        self.params = None
        self.quit = None
        self.filters = []
        self.filter_to_remove = []
        self.error = False

    def reg_pipe(self, pipe):
        self.pipe = pipe
        self.params = pipe.params
        self.quit = pipe.quit

    def add_filter(self, filter):
        """
        call reg_pipe first
        :param pipe:
        :return:
        """
        if not self.filters:
            self.filters.append(filter)
        else:
            last_filter = self.filters[-1]
            filter.in_queue = last_filter.out_queue
            self.filters.append(filter)

        filter.reg_sub_pipe(self)

    def init(self):
        self.error = False
        for f in self.filters:
            if not f.init():
                self.error = True
                break

        return not self.error

    def filter_finish(self, filter):
        self.filter_to_remove.append(filter)

    def work(self):
        try:
            while True:
                for f in self.filters:
                    f.do()

                if self.filter_to_remove:
                    for f in self.filter_to_remove:
                        self.filters.remove( f )
                    self.filter_to_remove = []

                if self.quit[0]:
                    break

                if not self.filters:
                    break

            return not self.error

        except Exception as e:
            import traceback
            # print(traceback.format_exc())
            logging.error('pipe work error\n%s',traceback.format_exc())
            self.params['error']={
                'code': ERROR_INTERNAL_ERROR,
                'msg': 'pipe work error: %s' % str(e)
            }

            return False