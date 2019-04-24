# coding=utf-8

from ..core.pipe_node import PipeNode
from ..processing_exception import *
import os, cv2
import requests
import logging

class PrepareFaceTrans(PipeNode):
    def __init__(self):
        super(PrepareFaceTrans, self).__init__()
        self.work_path = './work_path'

        self.work_dir = None


    def make_work_dir(self,work_path, video_id ):
        work_dir = os.path.join(work_path, video_id)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)

        return work_dir

    def download_pic(self, pic_url, save_to):
        try:
            response = requests.get(pic_url)
            response.raise_for_status()
            img = response.content
            with open(save_to, 'wb') as f:
                f.write(img)

        except Exception as e:
            logging.error('cant download pic file: %s' % str(e))
            self.error(ERROR_DOWNLOAD, 'cant download pic file: %s' % str(e))
            return False

        return True


    def init(self):
        # check if all parameters is present
        all_present = 'video_id'    in self.params and \
            'pic_url'               in self.params and \
            'template_id'           in self.params

        if not all_present:
            self.error(ERROR_PARAM, 'param missing')
            return False

        if 'fps' not in self.params:
            self.params['fps'] = '24'
        if 'trans_width' not in self.params:
            self.params['trans_width'] = '360'
        if 'bitrate' not in self.params:
            self.params['bitrate'] = '500k'


        #work_path = '/data/faceTrans'
        self.work_dir = self.make_work_dir(self.work_path, self.params['video_id'])
        self.params['work_dir'] = self.work_dir
        self.params['video_output'] = os.path.join(self.work_dir,'%s.mp4'% self.params['video_id'])

        logging.info('prepare work download')

        pic_file = os.path.join(self.work_dir, 'face.jpg')
        if not self.download_pic(self.params['pic_url'], pic_file):
            return False

        resized_pic = self.img_resize(pic_file)
        self.params['orig_face_pic'] = pic_file
        self.params['input_file'] = resized_pic

        logging.info('prepare work, input data: %s', str(self.params))

        return True

    def img_resize(self, pic_file):
        img = cv2.imread(pic_file)
        width = img.shape[1]
        height = img.shape[0]

        resize_width = self.params['trans_width']
        resize_width = int( int(resize_width) // 4 * 4)
        resize_height = int( (int(resize_width) / width * height)  // 4 * 4 )

        img_tmp = cv2.resize(img,(resize_width, resize_height))
        resized_img = os.path.join( self.work_dir, 'face_resize.jpg' )
        cv2.imwrite(resized_img,img_tmp)

        return resized_img



