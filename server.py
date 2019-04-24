# coding=utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.web
from service.face_handler import FaceHandler
import threading
import socket,logging, logging.handlers,os,time,signal
from processing.work_pool import WorkPool
from Utility.clear_disk import ClearDisk

HTTP_SERVER = None
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1

clear_disk = None

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            debug=False,
        )

        self.work_pool = WorkPool()

        handlers = [
            (r"/face", FaceHandler),
        ]

        super(Application,self).__init__(handlers,**settings)

def init_logging():
    log_file = 'videoprocess.log'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #create log path
    log_path = './log'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    #fh = logging.FileHandler(os.path.join(log_path, log_file))
    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, log_file), when='D', backupCount=7)
    sh = logging.StreamHandler()

    ###########This set the logging level that show on the screen#############
    #sh.setLevel(logging.DEBUG)
    #sh.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.info("Current log level is : %s",logging.getLevelName(logger.getEffectiveLevel()))

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    global clear_disk

    logging.info('Stopping http server')
    HTTP_SERVER.stop()

    logging.info('will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            clear_disk.de_init()
            logging.info('Shutdown')

    stop_loop()


def main():
    port = 6789

    ############init logging##############################
    init_logging()

    ############ free disk #############################
    global clear_disk
    clear_disk = ClearDisk()
    clear_disk.start()

    ############setting tornado server#####################
    global HTTP_SERVER

    try:
        HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
        HTTP_SERVER.listen(port)
    except Exception as ex:
        logging.error("Create and listen http server failed! Exception: %s", str(ex))
        quit()

    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ############start tornado server#######################
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit SVC-Master')


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("Ocurred Exception: %s" % str(ex))
        quit()
