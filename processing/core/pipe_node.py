#coding=utf-8

from .sub_pipe import SubPipe
import queue
import logging

class PipeNode():
    def __init__(self):
        self.pipe = None
        self.params = None

    def init(self):
        return True

    def reg_pipe(self, pipe):
        self.pipe = pipe
        self.params = pipe.params

    def error(self, code, msg):
        logging.error('code: %s, msg: %s', code, msg)
        self.params['error'] = {
            'code':code,
            'msg':msg
        }

    def do(self):
        return True


class Filter(PipeNode):
    Finish = SubPipe.Finish()
    def __init__(self):
        super(Filter, self).__init__()
        self.sub_pipe = None
        self.out_queue = queue.Queue()
        self.in_queue = None

    def init(self):
        return True

    def reg_sub_pipe(self, sub_pipe):
        self.sub_pipe = sub_pipe

        if self.pipe is None:
            self.pipe = sub_pipe.pipe
            self.params = sub_pipe.pipe.params

    def get_data(self):
        return self.in_queue.get()

    def send_data(self,data):
        self.out_queue.put(data)

    def do(self):
        return

    def finish(self, error = False):
        if error: # once error occur, sub pipe considered error, prevent other finish change error state
            self.error = error

        self.sub_pipe.filter_finish(self)
        self.send_data(self.Finish)


