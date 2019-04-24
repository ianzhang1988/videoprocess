# coding=utf-8

from ..core.pipe_node import Filter
import numpy as np
import cv2, os
from .gl_render.gl_render import GLRender
from .gl_render.coord_info import FaceInfo, FrameInfo
from processing.processing_exception import *
import logging

class GLRenderFilter(Filter):
    def __init__(self):
        super(GLRenderFilter, self).__init__()
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

        logging.info('gl render inited')

        self.width = self.params['width']
        self.height = self.params['height']
        print('width',self.width)

        self.render = GLRender( self.width, self.height )

        facetrans = self.fill_face_trans_data(self.facetrans)

        self.frame_count = facetrans.shape[0]
        #self.frame_count = 200
        self.set_face_frame_info(facetrans)

        self.inited = True

    def get_face_trans_data(self):
        fps = self.params['fps']
        template_id = int(self.params['template_id'])

        import libFaceSDK as face
        face.init("./2017-09-30-18-22-npd-83_fd0917_ert")
        #face_pic = self.params['input_file']

        face_pic = self.params['orig_face_pic']
        face_img = cv2.imread(face_pic)
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        point = face.align(face_img)

        if type(point) != np.ndarray:
            logging.warning('no face detect')
            self.error(ERROR_NO_FACE,'no face detect')
            return False

        resized_face_pic = self.params['input_file']
        resized_img = cv2.imread(resized_face_pic)

        facetrans = face.transform(int(fps), int(template_id))

        # convert points pos to resize pos
        facetrans_adjust = np.zeros(facetrans.shape, dtype=np.int32)

        h = face_img.shape[0]
        w = face_img.shape[1]
        resized_h = resized_img.shape[0]
        resized_w = resized_img.shape[1]

        scale_w = float(resized_w) / w
        scale_h = float(resized_h) / h

        for i in range(91):
            facetrans_adjust[:, 2 * i]      = facetrans[:, 2 * i] * scale_w
            facetrans_adjust[:, 2 * i+ 1]   = facetrans[:, 2 * i + 1] * scale_h

        # facetrans_adjust = facetrans_adjust.astype(dtype=np.int32)
        # facetrans = np.load('./facetrans.npy')

        if False:
            self.draw_landmark(face_img, facetrans, resized_img, facetrans_adjust)

        return facetrans_adjust

    def draw_landmark(self,  src_img,facetrans, resize_img, facetrans_adjust ):
        video_output = self.params['video_output']
        path = os.path.dirname(video_output)
        name_orig = os.path.basename(video_output)
        name = name_orig + '.jpg'
        name_resize = name_orig + '.resize.jpg'

        src_img_tmp = src_img.copy()
        resize_img_tmp = resize_img.copy()

        for i in range(91):
            x = facetrans[0, 2 * i]
            y = facetrans[0, 2 * i + 1]
            cv2.circle(src_img_tmp,(x,y), 2, (0,0,255),2)

            x = facetrans_adjust[0,  2 * i]
            y = facetrans_adjust[0,  2 * i + 1]
            cv2.circle(resize_img_tmp, (x, y), 2, (0, 0, 255), 2)

        cv2.imwrite(os.path.join(path, name), src_img_tmp)
        cv2.imwrite(os.path.join(path, name_resize), resize_img_tmp)


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
                # img_temp = img.copy()
                self.render.gl_render_draw(self.face_info, self.frame_info, self.counter)
                render_img = self.render.gl_get_data()

                # cvimg = cv2.cvtColor(render_img, cv2.COLOR_RGBA2BGR)
                # cv2.imshow('',cvimg)
                # cv2.waitKey(0)

                self.send_data(render_img)
                self.counter+=1
            else:
                self.render.uninit()
                self.finish()

        except Exception as e:
            import traceback
            #print(traceback.format_exc())
            logging.error('gl render error\n%s', traceback.format_exc())
            self.error( ERROR_INTERNAL_ERROR, str(e) )

            self.render.uninit()
            self.finish()


