#coding=utf-8

from ..core.pipe_node import Filter
import cv2 as cv
import logging

class InputOnePic(Filter):
    def __init__(self):
        super(InputOnePic, self).__init__()

    def set_img_size(self,width, height):
        self.params['width'] = width
        self.params['height'] = height

    def do(self):

        input_file = self.params['input_file']
        img = cv.imread(input_file)

        logging.info('input image read')

        self.set_img_size(img.shape[1],img.shape[0])

        self.send_data(img)

        self.finish()







