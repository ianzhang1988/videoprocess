#coding=utf-8
import logging
from ..processing_exception import *

class Pipe():
    """
    pipe for video process
    """
    def __init__(self):
        # parameters used throughout pipe for all node filter, need to be mutable object
        self.params = None
        self.begin_nodes = []
        self.finish_nodes = []
        self.sub_pipe = None
        self.super_finish_nodes = [] # do it any way
        self.quit = [False] # mutable object
        self.error = False

    def init(self):
        """
        initialize all node filter in pipe
        """
        logging.info('Pipe init')

        try:
            self.error = False

            for n in self.begin_nodes:
                if not n.init():
                    logging.error('Pipe init begin node error')
                    self.error = True
                    break

            logging.info('Pipe init begin node inited')

            if not self.error:
                if not self.sub_pipe.init():
                    logging.error('Pipe init sub pipe error')
                    self.error = True

            logging.info('Pipe init sub pipe inited')

            if not self.error:
                logging.error('Pipe init finish node error')
                for n in self.finish_nodes:
                    if not n.init():
                        break

            logging.info('Pipe init finish node inited')

            for n in self.super_finish_nodes:
                n.init()

        except Exception as e:
            import traceback
            # print(traceback.format_exc())
            logging.error('pipe init error\n%s', traceback.format_exc())

            self.params['error'] = {
                'code': ERROR_INTERNAL_ERROR,
                'msg': 'pipe init error: %s' % str(e)
            }

        logging.info('Pipe init finish')

    def add_begin_node(self, node):
        self.begin_nodes.append(node)
        node.reg_pipe(self)

    def add_finish_node(self, node):
        self.finish_nodes.append(node)
        node.reg_pipe(self)

    def add_super_finish_node(self, node):
        self.super_finish_nodes.append(node)
        node.reg_pipe(self)

    def add_sub_pipe(self, sub_pipe):
        self.sub_pipe = sub_pipe
        sub_pipe.reg_pipe(self)

    def work(self):
        logging.error('Pipe start work')
        try:
            if not self.error:
                for n in self.begin_nodes:
                    if not n.do():
                        logging.error('Pipe begin nodes work error')
                        self.error = True
                        break

            logging.info('Pipe begin nodes work done')
            if self.quit[0]:
                return

            if not self.error:
                if not self.sub_pipe.work():
                    logging.error('Pipe sub pipe work error')
                    self.error = True

            logging.info('Pipe sub pipe work done')
            if self.quit[0]:
                return

            if not self.error:
                for n in self.finish_nodes:
                    if not n.do():
                        logging.error('Pipe finish nodes work error')
                        self.error = True
                        break

            logging.info('Pipe finish nodes work done')
            # do it anyway
            for n in self.super_finish_nodes:
                n.do()

            logging.info('Pipe super finish nodes work done')

        except Exception as e:
            import traceback
            # print(traceback.format_exc())
            logging.error('pipe work error\n%s',traceback.format_exc())

            self.params['error'] = {
                'code': ERROR_INTERNAL_ERROR,
                'msg': 'pipe work error: %s' % str(e)
            }



