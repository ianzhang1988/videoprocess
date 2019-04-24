# coding=utf-8

from ..core.pipe_node import Filter
import numpy as np
import cv2
# from .gl_render.gl_render import GLRender
from .gl_render.coord_info import FaceInfo, FrameInfo
from processing.processing_exception import *
import logging

class FakeRenderFilter(Filter):
    def __init__(self):
        super(FakeRenderFilter, self).__init__()
        self.inited = False

    def init(self):
        self.counter = 0
        self.img = None

        template_id = int(self.params['template_id'])
        self.params['srt'] = './material/srt/video%s.srt' % template_id
        self.params['audio'] = './material/voice/video%s.wav' % template_id

        self.facetrans = self.get_face_trans_data()
        if self.facetrans is False:
            return False

        return True

    def _init(self):
        if self.inited:
            return

        self.width = self.params['width']
        self.height = self.params['height']
        print('width',self.width)

        # self.render = GLRender( self.width, self.height )

        facetrans = self.fill_face_trans_data(self.facetrans)

        self.frame_count = facetrans.shape[0]
        #self.frame_count = 200
        self.set_face_frame_info(facetrans)

        self.inited = True

    def get_face_trans_data(self):
        fps = self.params['fps']
        template_id = int(self.params['template_id'])

        import libFaceSDK as face
        face.init("/opt/borui/FaceSDK/model/2017-09-30-18-22-npd-83_fd0917_ert")
        face_pic = self.params['input_file']
        point = face.align(face_pic)

        if type(point) != np.ndarray:
            #raise NoFaceDetected()
            self.error(ERROR_NO_FACE,'no face detect')
            return False

        facetrans = face.transform(int(fps), int(template_id))

        # facetrans = np.load('./facetrans.npy')

        return facetrans

    def set_face_frame_info(self, facetrans):
        self.face_info = FaceInfo()
        self.face_info.width = self.width
        self.face_info.height = self.height
        self.face_info.faces = [facetrans[1, :]]

        self.frame_info = FrameInfo()
        self.frame_info.width = self.width
        self.frame_info.width = self.height
        self.frame_info.frames = [facetrans[i, :] for i in range(facetrans.shape[0])]
        self.frame_info.set_material()

    def fill_face_trans_data(self, facetrans):
        facetrans_fill = np.zeros((facetrans.shape[0], facetrans.shape[1] + 8),dtype=np.int32)
        facetrans_fill[:,:facetrans.shape[1]] = facetrans
        facetrans_fill[:, 182] = 0
        facetrans_fill[:, 183] = 0
        facetrans_fill[:, 184] = 0
        facetrans_fill[:, 185] = self.height
        facetrans_fill[:, 186] = self.width
        facetrans_fill[:, 187] = self.height
        facetrans_fill[:, 188] = self.width
        facetrans_fill[:, 189] = 0

        return facetrans_fill

    def do(self):
        try:
            self._init()

            if self.img is None:
                self.img = self.get_data()
                rgba = cv2.cvtColor(self.img, cv2.COLOR_BGRA2RGBA)
                self.face_info.rgba = rgba

            if self.counter < self.frame_count:
                render_img = self.face_info.rgba
                # self.render.gl_render_draw(self.face_info, self.frame_info, self.counter)
                # render_img = self.render.gl_get_data()

                # cvimg = cv2.cvtColor(render_img, cv2.COLOR_RGBA2BGR)
                # cv2.imshow('',cvimg)
                # cv2.waitKey(0)

                self.send_data(render_img)
                self.counter+=1
            else:
                # self.render.uninit()
                self.finish()

        except Exception as e:
            import traceback
            #print(traceback.format_exc())
            logging.error('gl render error\n%s', traceback.format_exc())
            self.error( ERROR_INTERNAL_ERROR, str(e) )

            # self.render.uninit()
            self.finish()


