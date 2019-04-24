# coding=utf-8

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT import *
#from OpenGL.arrays import vbo
#from OpenGLContext.arrays import *

import numpy as np
import cv2
import sys

from .gl_draw import GLDraw

class GLRender(  ):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        glutInit(sys.argv)

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(width, height)
        glutCreateWindow(b"OpenGL Offscreen")
        glutHideWindow()

        self.gl_draw = GLDraw(width, height)

        self.gl_offscreen_frame_buf = glGenFramebuffers(1)
        self.draw_temp_tex = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.draw_temp_tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_2D, 0)


    def gl_render_draw(self, face_info, frame_info, frame_idx ):
        glBindFramebuffer(GL_FRAMEBUFFER, self.gl_offscreen_frame_buf)
        glViewport(0, 0, self.width, self.height)

        # draw to texture
        texture_name = self.gl_draw.gl_draw_to_texture( face_info, self.width, self.height)
        glFlush()

        # draw to change face
        in_tex = texture_name
        out_tex = self.draw_temp_tex

        for i in range(face_info.face_count):
            self.gl_draw.gl_draw_change_face( in_tex, out_tex, face_info, frame_info, i, frame_idx)
            in_tex, out_tex = out_tex, in_tex

        glFlush()

        # 翻转
        # self.gl_draw.gl_draw_flip_y_to_texture( in_tex, out_tex,self.width, self.height)
        # in_tex, out_tex = out_tex, in_tex

        # glFlush()

        return in_tex

    def gl_get_data(self):
        data = glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        glFlush()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        img = np.fromstring(data, dtype=np.uint8).reshape((self.height, self.width, 4))
        # cvt_img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img

    def uninit(self):
        self.gl_draw.gl_draw_context_uninit()










