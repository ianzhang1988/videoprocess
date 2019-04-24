# coding=utf-8

from ..core.pipe_node import Filter
import numpy as np
import cv2 as cv
from skvideo.io import FFmpegWriter
import logging
from ..processing_exception import *

class EncodeVideo(Filter):
    def __init__(self):
        super(EncodeVideo, self).__init__()
        self.counter = 0

    def init(self):
        self.out_put_file = self.params['video_output']
        self.fps = self.params['fps']
        self.bit_rate = self.params['bitrate']
        self.width = self.params['trans_width']
        #self.height = self.params['trans_height']

        print(self.params)

        self.srt = self.params['srt']
        self.audio = self.params['audio']


        # X264 MP4V avc1 XVID MJPG
        # fourcc = cv.VideoWriter_fourcc(*'XVID')
        # self.out = cv.VideoWriter('%s.avi'%self.out_put_file, fourcc, self.fps, (640, 480), True)

        self.out = FFmpegWriter(self.out_put_file, inputdict={'-i':self.audio,'-r':str(self.fps), '-pix_fmt':'rgba'},
                                outputdict={'-vcodec': 'libx264','-profile:v':'main','-preset':'ultrafast', '-r':str(self.fps) ,'-b:v': str(self.bit_rate),
                                            '-vf':'format=yuv420p,scale=%s:%s,subtitles=%s'% (self.width , '-4',self.srt)},
                                verbosity=1)

        return True

    def do(self):
        img = self.get_data()

        if img is self.Finish:
            #self.out.release()
            self.out.close()
            self.finish()
            return
        # img = cv.resize(img, (640,480))

        #cv.imwrite( '%s_%s.jpg' %(self.out_put_file , self.counter), img )
        # self.out.write(img.astype('uint8'))

        try:
            self.out.writeFrame(img.astype('uint8'))
        except Exception as e:
            import traceback
            #print(traceback.format_exc())
            logging.error('gl render error\n%s', traceback.format_exc())
            self.error( ERROR_INTERNAL_ERROR, str(e) )

            # self.render.uninit()
            self.finish()

        self.counter += 1


