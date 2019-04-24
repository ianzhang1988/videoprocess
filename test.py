# coding=utf-8

from processing.core.build_pipe import build_pipe
from processing.work_pool import WorkPool
import logging,logging.handlers,os

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

    ###########This set the logging level that show on the screen#############R)
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.info("Current log level is : %s",logging.getLevelName(logger.getEffectiveLevel()))

init_logging()

params = {
    'video_id':'90367798',
    'fps':30,
    #'length':5,
    # 'input_file':'./cage.jpg',
    'pic_url':'http://10.10.76.179:7777/testpic/cage.jpg',
    #'video_output': './testout/output',
    #'trans_width': '360',
    #'trans_height': '885',
    #'bitrate': '500k',
    'template_id':'2'
}

def test_pipe():
    pipe = build_pipe('test2', params)
    pipe.work()
    print(pipe.params)

def test_work_pool():
    pool = WorkPool()
    pool.add_job(params)
    params['video_id']='10001'
    ret = pool.add_job(params)
    print('---------- ret:',ret)
    params['video_id'] = '10002'
    ret = pool.add_job(params)
    print('---------- ret:', ret)
    params['video_id'] = '10003'
    ret = pool.add_job(params)
    print('---------- ret:', ret)
    pool.quit()

# test_work_pool()
# test_pipe()

params = {
    'video_id':'90367798',
    'fps':24,
    #'length':5,
    # 'input_file':'./cage.jpg',
    'pic_url':'http://10.10.76.179:7777/testpic/cage.jpg',
    'video_output': './output',
    'trans_width': '360',
    #'trans_height': '885',
    'bitrate': '500k',
    'template_id':'4'
}

import cv2
def resize_pic( file,  trans_width = 360):
    img = cv2.imread(file)
    width = img.shape[1]
    height = img.shape[0]

    resize_width = trans_width
    resize_width = int(int(resize_width) // 4 * 4)
    resize_height = int((int(resize_width) / width * height) // 4 * 4)

    img_tmp = cv2.resize(img, (resize_width, resize_height))

    resized_img = os.path.join('output', os.path.basename(file) + '.resize.jpg')
    cv2.imwrite(resized_img, img_tmp)
    return resized_img


def test_rendder():
    pic_name = os.listdir('test_pic')
    test_pic = [os.path.join('./test_pic', i) for i in pic_name]

    for i, file in enumerate(test_pic):
        logging.info('file %s', file)

        resize_file = resize_pic(file)

        params['video_id'] = os.path.basename(file)
        params['orig_face_pic'] = file
        params['input_file'] = resize_file
        params['video_output'] = os.path.join('./output', params['video_id'] + '.mp4')

        pipe = build_pipe('test', params)
        pipe.work()
        print(pipe.params)
        logging.info('-------------------------------\n\n\n')

test_rendder()