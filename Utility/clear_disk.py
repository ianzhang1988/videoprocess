import threading
import time, os, re
import logging
import shutil
import traceback

"""
for now one video is around 1.18643395478 M
set 1T as threshold, we can hold 880k video
lets set 500k video as a limit
"""

class ClearDisk():
    def __init__(self):
        self.path = './work_path' # same as videoprocess\processing\component\node_prepare_face_trans.py
        self.work_thread = None
        self.working = None
        self.counter = 0
        self.time_out = 3600*12

        self.video_num_limit = 500000
        # self.delete_num = 2000

    def start(self):
        self.working = True
        self.work_thread = threading.Thread(target=self._work)
        self.work_thread.start()

    def clear(self):
        try:
            logging.info('check disk space')
            vid_folder_list = os.listdir(self.path)
            if len(vid_folder_list) <= self.video_num_limit:
                logging.info('vidoe num %s less than %s, disk space ok', len(vid_folder_list), self.video_num_limit )
                return

            logging.info('vidoe num %s more than %s, free space', len(vid_folder_list), self.video_num_limit )

            delete_num = len(vid_folder_list) - self.video_num_limit

            vid_num_list = [int(i) for i in vid_folder_list if re.fullmatch('\d+',i)]
            vid_num_sorted = sorted(vid_num_list)

            delete_list = [str(i) for i in vid_num_sorted[:delete_num]]

            logging.info('delete %s', str(delete_list))

            for f in delete_list:
                delete_path = os.path.join(self.path, f)
                shutil.rmtree(delete_path)
        except Exception as e:
            logging.error('clear disk error:\n%s\n', traceback.format_exc())

    def _work(self):
        logging.info('disk check work start')
        while self.working:
            time.sleep(1)
            if self.counter < self.time_out:
                self.counter += 1
                continue

            self.counter = 0
            self.clear()
        logging.info('disk check work quit')

    def de_init(self):
        self.working = False
        self.work_thread.join()


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    cd = ClearDisk()
    cd.video_num_limit = 2000
    cd.time_out = 30
    cd.clear()

    cd.start()

    time.sleep(3600)

    cd.de_init()



