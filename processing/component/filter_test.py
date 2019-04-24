# coding=utf-8

from ..core.pipe_node import Filter
import numpy as np
import cv2 as cv

class TestFilter(Filter):
    def __init__(self):
        super(TestFilter, self).__init__()

    def do(self):
        img = self.get_data()

        fps = self.params['fps']
        length = self.params['length']

        frame_count = fps * length

        for i in range(frame_count):
            img_temp = img.copy()
            cv.rectangle(img_temp,(i*5, 10), (i*5+200, 140), (255,255,255))

            self.send_data(img_temp)

        self.finish()
