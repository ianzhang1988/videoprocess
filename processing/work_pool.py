#coding=utf-8

from multiprocessing import Process
import logging
from .core.build_pipe import build_pipe

def worker_process(params):
    # pipe work
    try:
        pipe = build_pipe('face_trans', params)
        #pipe = build_pipe('test2', params)
        pipe.work()
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        logging.error('pipe work error',str(e))


class WorkPool():
    def __init__(self):
        self.process_num_limit = 10
        self.process = []

    def add_job(self, params):
        finished = []
        for p in self.process:
            if p.exitcode is not None:
                finished.append(p)

        for p in finished:
            self.process.remove(p)

        if len(self.process) >= self.process_num_limit:
            return False

        logging.info('WorkPool add job %s', str(params))
        p = Process(target=worker_process, args=(params,) )
        p.start()
        self.process.append(p)

        return True


    def quit(self):
        logging.info('WorkPool Quitting')

        print(self.process)
        for p in self.process:
            p.join()

        logging.info('WorkPool Quit')
