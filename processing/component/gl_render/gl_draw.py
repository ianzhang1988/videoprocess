# coding=utf-8

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT import *
#from OpenGL.arrays import vbo
#from OpenGLContext.arrays import *
from ctypes import *

import numpy as np
import cv2, math

g_allIndices = [
# 180 triangles
    91,92,83,
    83,92,84,
    84,92,85,
    85,92,86,
    86,92,93,
    86,93,87,
    87,93,88,
    88,93,89,
    89,93,94,
    90,89,94,
    90,94,91,
    90,91,83,
    10,15,14,
    34,35,43,
    71,44,70,
    20,24,90,
    22,20,90,
    38,40,42,
    39,41,13,
    42,40,50,
    36,34,37,
    42,34,38,
    86,66,74,
    15,10,39,
    70,85,71,
    19,90,24,
    28,32,89,
    25,19,24,
    12,31,14,
    34,39,37,
    34,43,39,
    37,10,26,
    13,17,9,
    76,17,13,
    32,29,33,
    77,76,41,
    17,75,11,
    27,33,11,
    27,11,65,
    16,9,17,
    51,45,41,
    11,16,17,
    87,81,82,
    49,51,43,
    78,79,87,
    41,76,13,
    89,75,88,
    76,75,17,
    72,73,44,
    85,72,86,
    44,73,58,
    85,72,71,
    73,74,59,
    85,73,72,
    74,66,59,
    85,74,73,
    85,86,74,
    43,41,39,
    73,59,58,
    55,82,60,
    6,68,40,
    48,42,50,
    40,70,44,
    8,0,4,
    23,20,22,
    35,34,42,
    38,6,40,
    69,85,70,
    84,85,69,
    40,44,50,
    71,72,44,
    40,69,70,
    68,84,69,
    6,67,68,
    83,84,67,
    40,68,69,
    67,84,68,
    18,64,1,
    83,67,64,
    67,1,64,
    21,24,20,
    67,6,1,
    2,36,19,
    6,5,1,
    0,7,3,
    83,62,18,
    83,64,62,
    64,18,62,
    1,5,23,
    1,23,18,
    5,21,23,
    18,22,83,
    18,23,22,
    23,21,20,
    3,7,25,
    19,25,7,
    25,21,3,
    21,25,24,
    7,8,2,
    26,19,36,
    26,90,19,
    5,3,21,
    5,6,0,
    5,0,3,
    36,38,34,
    6,4,0,
    6,38,4,
    0,8,7,
    4,38,8,
    7,2,19,
    8,38,2,
    26,36,37,
    2,38,36,
    45,61,80,
    39,10,37,
    12,9,16,
    13,15,39,
    13,9,15,
    22,90,83,
    32,63,89,
    26,30,90,
    29,12,16,
    26,31,30,
    26,10,14,
    26,14,31,
    15,9,14,
    30,28,90,
    30,31,29,
    32,27,63,
    33,16,11,
    90,28,89,
    27,65,63,
    63,65,89,
    32,33,27,
    32,28,29,
    33,29,16,
    28,30,29,
    31,12,29,
    14,9,12,
    88,76,77,
    75,65,11,
    88,75,76,
    89,65,75,
    35,49,43,
    61,81,80,
    77,41,45,
    41,43,51,
    78,45,79,
    77,78,87,
    77,45,78,
    42,48,35,
    46,35,48,
    49,35,46,
    59,66,55,
    82,66,86,
    55,66,82,
    87,82,86,
    77,87,88,
    81,60,82,
    81,61,60,
    80,81,87,
    79,80,87,
    79,45,80,
    78,79,87,
    44,58,56,
    58,59,56,
    56,59,54,
    59,55,54,
    54,55,60,
    54,60,57,
    57,60,61,
    57,61,45,
    45,51,53,
    51,49,53,
    53,49,47,
    49,46,47,
    47,46,48,
    47,48,52,
    48,50,52,
    52,50,44,
]

g_faceIndices = [
# 180 triangles
    91,92,83,
    83,92,84,
    84,92,85,
    85,92,86,
    86,92,93,
    86,93,87,
    87,93,88,
    88,93,89,
    89,93,94,
    90,89,94,
    90,94,91,
    90,91,83,
    10,15,14,
    34,35,43,
    71,44,70,
    20,24,90,
    22,20,90,
    38,40,42,
    39,41,13,
    42,40,50,
    36,34,37,
    42,34,38,
#    86,66,74,
    15,10,39,
    70,85,71,
    19,90,24,
    28,32,89,
    25,19,24,
    12,31,14,
    34,39,37,
    34,43,39,
    37,10,26,
    13,17,9,
    76,17,13,
    32,29,33,
    77,76,41,
    17,75,11,
    27,33,11,
    27,11,65,
    16,9,17,
    51,45,41,
    11,16,17,
#    87,81,82,
    49,51,43,
    78,79,87,
    41,76,13,
    89,75,88,
    76,75,17,
    72,73,44,
#    85,72,86,
    44,73,58,
    85,72,71,
    73,74,59,
#    85,73,72,
    74,66,59,
#    85,74,73,
#    85,86,74,
    43,41,39,
    73,59,58,
    55,82,60,
    6,68,40,
    48,42,50,
    40,70,44,
    8,0,4,
    23,20,22,
    35,34,42,
    38,6,40,
    69,85,70,
    84,85,69,
    40,44,50,
    71,72,44,
    40,69,70,
    68,84,69,
    6,67,68,
    83,84,67,
    40,68,69,
    67,84,68,
    18,64,1,
    83,67,64,
    67,1,64,
    21,24,20,
    67,6,1,
    2,36,19,
    6,5,1,
    0,7,3,
    83,62,18,
    83,64,62,
    64,18,62,
    1,5,23,
    1,23,18,
    5,21,23,
    18,22,83,
    18,23,22,
    23,21,20,
    3,7,25,
    19,25,7,
    25,21,3,
    21,25,24,
    7,8,2,
    26,19,36,
    26,90,19,
    5,3,21,
    5,6,0,
    5,0,3,
    36,38,34,
    6,4,0,
    6,38,4,
    0,8,7,
    4,38,8,
    7,2,19,
    8,38,2,
    26,36,37,
    2,38,36,
    45,61,80,
    39,10,37,
    12,9,16,
    13,15,39,
    13,9,15,
    22,90,83,
    32,63,89,
    26,30,90,
    29,12,16,
    26,31,30,
    26,10,14,
    26,14,31,
    15,9,14,
    30,28,90,
    30,31,29,
    32,27,63,
    33,16,11,
    90,28,89,
    27,65,63,
    63,65,89,
    32,33,27,
    32,28,29,
    33,29,16,
    28,30,29,
    31,12,29,
    14,9,12,
    88,76,77,
    75,65,11,
    88,75,76,
    89,65,75,
    35,49,43,
    61,81,80,
    77,41,45,
    41,43,51,
    78,45,79,
    77,78,87,
    77,45,78,
    42,48,35,
    46,35,48,
    49,35,46,
    59,66,55,
#    82,66,86,
    55,66,82,
#    87,82,86,
    77,87,88,
    81,60,82,
    81,61,60,
#    80,81,87,
    79,80,87,
    79,45,80,
    78,79,87,
    44,58,56,
    58,59,56,
    56,59,54,
    59,55,54,
    54,55,60,
    54,60,57,
    57,60,61,
    57,61,45,
    45,51,53,
    51,49,53,
    53,49,47,
    49,46,47,
    47,46,48,
    47,48,52,
    48,50,52,
    52,50,44,
]

ATTRIB_VX  = 0
ATTRIB_TEX = 1

vertices = np.array([-1.0,1.0, 1.0,1.0 ,-1.0,-1.0,  1.0,-1.0,], dtype=np.float32)
textureCoordinates = np.array([0.0,1.0, 1.0,1.0, 0.0,0.0, 1.0,0.0,], dtype=np.float32)
textureCoordinates_flip = np.array([0.0,0.0, 1.0,0.0, 0.0,1.0, 1.0,1.0,], dtype=np.float32)

class GLDraw():
    FACE_POINTS_NUM = 95
    MOUTH_CORRECTION = 2
    ALL_TRIANGELS_NUM = 180
    allIndices = g_allIndices
    FACE_TRIANGLES_NUM = 171
    faceIndices = g_faceIndices

    def __init__(self,width, height):
        self.uninit_flag = False

        self.width = width
        self.height = height

        # glutInit(sys.argv)
        #
        # glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        # glutInitWindowSize(width, height)
        # glutCreateWindow(b"OpenGL Offscreen")
        # glutHideWindow()

        self.compile_shader()
        self.compile_program()

        self.src_tex = 0
        self.rgba_tex = 0
        self.draw_src_tex = 0
        self.draw_rgba_tex = 0
        self.mouth_tex = 0
        self.tongue_tex = 0

        self.matrix =   [[ 1. , 0. , 0. , 0.],
                         [ 0. , 1. , 0. , 0.],
                         [ 0. , 0. , 1. , 0.],
                         [ 0. , 0. , 0. , 1.]]

        self.upper_no_rotate_t = np.zeros(8, dtype=np.float32)
        self.upper_t = np.zeros(8, dtype=np.float32)

    def compile_shader(self):
        self.kPassThroughVertexShader = compileShader("""
        attribute vec4 position;
        attribute vec2 texCoord;
        uniform mat4 renderTransform;
        varying vec2 texCoordVarying;
        void main()
        {
            gl_Position = renderTransform * position;// * renderTransform;
            texCoordVarying = texCoord;
        }""", GL_VERTEX_SHADER)

        self.kPassThroughFragmentShaderRGB = compileShader("""
        varying vec2 texCoordVarying;
        uniform sampler2D SamplerRGB;
        void main()
        {
            gl_FragColor.rgba = texture2D(SamplerRGB, texCoordVarying).rgba;
        }""", GL_FRAGMENT_SHADER)

        self.ChangeFaceFragmentShader = compileShader("""
        varying vec2 texCoordVarying;
        uniform sampler2D SamplerRGB;
        uniform sampler2D SamplerMouth; 
        uniform float a; 
        void main() 
        { 
            if (a > 0.000001) { 
                gl_FragColor.rgba = texture2D(SamplerRGB, texCoordVarying).rgba;
            } else { 
                gl_FragColor.rgba = texture2D(SamplerMouth, texCoordVarying).rgba;
            }
        }""", GL_FRAGMENT_SHADER)

        self.kPassThroughVertexFlipYShader = compileShader("""
        attribute vec4 position; 
        attribute vec2 texCoord; 
        varying vec2 textureCoordinate; 
        void main() 
        { 
            gl_Position = position;
            textureCoordinate = texCoord;
        }""", GL_VERTEX_SHADER)

        self.kPassThroughFragmentFlipYShader = compileShader("""
        varying vec2 textureCoordinate;
        uniform sampler2D SamplerRGB;
        void main()
        {
            gl_FragColor = texture2D(SamplerRGB, textureCoordinate);
        }""", GL_FRAGMENT_SHADER)

    def compile_program(self):
        # -------- draw texture --------
        self.gl_draw_texture_program = compileProgram(self.kPassThroughVertexShader, self.kPassThroughFragmentShaderRGB)

        self.gl_draw_texture_param_renderTransform = glGetUniformLocation(self.gl_draw_texture_program, "renderTransform")
        self.gl_draw_texture_param_SamplerRGB = glGetUniformLocation(self.gl_draw_texture_program, "SamplerRGB")

        #glUseProgram(self.gl_draw_texture_program)
        glBindAttribLocation(self.gl_draw_texture_program, ATTRIB_VX, "position")
        glBindAttribLocation(self.gl_draw_texture_program, ATTRIB_TEX, "texCoord")
        #glUseProgram(0)

        # -------- draw change --------
        self.gl_draw_change_program = compileProgram(self.kPassThroughVertexShader, self.ChangeFaceFragmentShader)

        self.gl_draw_change_param_renderTransform = glGetUniformLocation(self.gl_draw_change_program,'renderTransform')
        self.gl_draw_change_param_SamplerRGB = glGetUniformLocation(self.gl_draw_change_program, 'SamplerRGB')
        self.gl_draw_change_param_SamplerMouth = glGetUniformLocation(self.gl_draw_change_program, 'SamplerMouth')
        self.gl_draw_change_param_A = glGetUniformLocation(self.gl_draw_change_program, 'a')

        #glUseProgram(self.gl_draw_change_program)
        glBindAttribLocation(self.gl_draw_change_program, ATTRIB_VX, "position")
        glBindAttribLocation(self.gl_draw_change_program, ATTRIB_TEX, "texCoord")
        #glUseProgram(0)

        # -------- draw flip --------
        self.gl_draw_flip_y_program = compileProgram(self.kPassThroughVertexFlipYShader, self.kPassThroughFragmentFlipYShader)

        self.gl_draw_flip_y_vertex_id = glGetUniformLocation(self.gl_draw_flip_y_program, 'position')
        self.gl_draw_flip_y_texture_id = glGetUniformLocation(self.gl_draw_flip_y_program, 'texCoord')
        self.gl_draw_flip_y_param_SamplerRGB = glGetUniformLocation(self.gl_draw_flip_y_program, 'SamplerRGB')

        glBindAttribLocation(self.gl_draw_flip_y_program, ATTRIB_VX, "position")
        glBindAttribLocation(self.gl_draw_flip_y_program, ATTRIB_TEX, "texCoord")

    def gl_draw_create_rgba_texture(self, w, h, buffer=None):
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glBindTexture(GL_TEXTURE_2D, 0)

        return tex

    def gl_draw_to_texture(self, face_info, width, height):
        # gl_offscreen_frame_buf = glGenFramebuffers(1)
        # glBindFramebuffer(GL_FRAMEBUFFER, gl_offscreen_frame_buf)
        glViewport(0, 0, width, height)

        self.draw_src_tex = self.gl_draw_create_rgba_texture(width, height)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.draw_src_tex, 0)

        glUseProgram(self.gl_draw_texture_program)

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.src_tex = self.gl_draw_create_rgba_texture(face_info.width, face_info.height, face_info.rgba)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.src_tex)

        glUniform1i(self.gl_draw_texture_param_SamplerRGB, 1)
        glUniformMatrix4fv(self.gl_draw_texture_param_renderTransform, 1, GL_FALSE, self.matrix)

        glEnableVertexAttribArray(ATTRIB_VX)
        glEnableVertexAttribArray(ATTRIB_TEX)

        # glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ids[0])
        # glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2*sizeof(GLfloat), c_void_p(0))
        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), vertices)

        # glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ids[1])
        # glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2*sizeof(GLfloat), c_void_p(0))
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), textureCoordinates)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glFlush()

        glDisableVertexAttribArray(ATTRIB_VX)
        glDisableVertexAttribArray(ATTRIB_TEX)

        # data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)

        glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        # glBindFramebuffer(GL_FRAMEBUFFER, 0)

        return self.draw_src_tex

    def gl_draw_flip_y_to_texture(self, in_tex, out_tex, width, height):
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, out_tex, 0)

        glUseProgram(self.gl_draw_flip_y_program)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, in_tex)
        glUniform1i(self.gl_draw_flip_y_param_SamplerRGB, 1)
        glEnableVertexAttribArray(ATTRIB_VX)
        glEnableVertexAttribArray(ATTRIB_TEX)

        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), vertices)
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), textureCoordinates_flip)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glDisableVertexAttribArray(ATTRIB_VX)
        glDisableVertexAttribArray(ATTRIB_TEX)
        glBindTexture(GL_TEXTURE_2D, 0)

    def gl_draw_change_face(self, in_tex, out_tex, face_info, frame_info, face_idx, frame_idx ):
        cur_face_coordinates = face_info.faces[face_idx]#.face_coordinates
        change_face_coordinates = frame_info.frames[frame_idx]#.face_coordinates

        cur_face_vertex_pos = np.zeros(200, dtype=np.float32)
        cur_face_texture_pos = np.zeros(200, dtype=np.float32)
        cur_background_face_vertex_pos = np.zeros(200, dtype=np.float32)

        for n in range(self.FACE_POINTS_NUM):
            cur_face_vertex_pos[0+n*2] = (change_face_coordinates[0+n*2]*1.0/face_info.width)*2.0-1.0
            cur_face_vertex_pos[1 + n * 2] = (change_face_coordinates[1 + n * 2] * 1.0 / face_info.height) * 2.0 - 1.0

            cur_face_texture_pos[0 + n * 2] = cur_face_coordinates[0 + n * 2] * 1.0 / face_info.width
            cur_face_texture_pos[1 + n * 2] = cur_face_coordinates[1 + n * 2] * 1.0 / face_info.height

            cur_background_face_vertex_pos[0 + n * 2] = (cur_face_coordinates[0 + n * 2] * 1.0 / face_info.width) * 2.0 - 1.0
            cur_background_face_vertex_pos[1 + n * 2] = (cur_face_coordinates[1 + n * 2] * 1.0 / face_info.height) * 2.0 - 1.0

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, out_tex, 0)
        glUseProgram(self.gl_draw_change_program)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUniformMatrix4fv(self.gl_draw_change_param_renderTransform, 1, GL_FALSE, self.matrix)

        glEnableVertexAttribArray(ATTRIB_VX)
        glEnableVertexAttribArray(ATTRIB_TEX)

        # 画舌头
        glUniform1f(self.gl_draw_change_param_A, 0.0)
        self.tongue_tex = self.gl_draw_create_rgba_texture( frame_info.tongue.width, frame_info.tongue.height, frame_info.tongue.data)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.tongue_tex)
        glUniform1i(self.gl_draw_change_param_SamplerMouth, 3)

        vertices = np.array([
            cur_face_vertex_pos[58 * 2], cur_face_vertex_pos[55 * 2 + 1],
            cur_face_vertex_pos[61 * 2], cur_face_vertex_pos[55 * 2 + 1],
            cur_face_vertex_pos[58 * 2], cur_face_vertex_pos[46 * 2 + 1], # 50
            cur_face_vertex_pos[61 * 2], cur_face_vertex_pos[46 * 2 + 1], # 51
        ], dtype=np.float32)


        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), vertices)
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), textureCoordinates)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        # 画上牙
        glUniform1f(self.gl_draw_change_param_A, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.mouth_tex = self.gl_draw_create_rgba_texture( frame_info.teeth.width, frame_info.teeth.height, frame_info.teeth.data)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.mouth_tex)
        glUniform1i(self.gl_draw_change_param_SamplerMouth, 2)

        upper_no_rotate_t = self.upper_no_rotate_t
        upper_t = self.upper_t

        if frame_idx == 0:
            # 4:left mouth corner 45: right mouth corner
            left_y = cur_face_vertex_pos[44 * 2 + 1]
            right_y = cur_face_vertex_pos[45 * 2 + 1]
            z_angle = 0.0
            x_dis = cur_face_vertex_pos[45 * 2] - cur_face_vertex_pos[44 * 2]
            y_dis = abs(left_y - right_y)
            z_angle = -self.MOUTH_CORRECTION * math.atan(y_dis / x_dis) * 180.0 / math.pi


            upper_no_rotate_t[0] = cur_face_vertex_pos[44 * 2]
            upper_no_rotate_t[1] = cur_face_vertex_pos[58 * 2 + 1]
            upper_no_rotate_t[2] = cur_face_vertex_pos[45 * 2]
            upper_no_rotate_t[3] = cur_face_vertex_pos[58 * 2 + 1]
            upper_no_rotate_t[4] = cur_face_vertex_pos[44 * 2]
            upper_no_rotate_t[5] = cur_face_vertex_pos[48 * 2 + 1]
            upper_no_rotate_t[6] = cur_face_vertex_pos[45 * 2]
            upper_no_rotate_t[7] = cur_face_vertex_pos[48 * 2 + 1]

            # uniform width and height
            upper_teeth_radio = 3.985 # teeth  w/h
            y_dis_correct = x_dis / upper_teeth_radio

            if y_dis_correct < (cur_face_vertex_pos[58 * 2 + 1] - cur_face_vertex_pos[48 * 2 + 1]):
                upper_no_rotate_t[1] = upper_no_rotate_t[3] = cur_face_vertex_pos[48 * 2+1] + y_dis_correct

            # center point
            center_x = (upper_no_rotate_t[0] + upper_no_rotate_t[2]) / 2.0
            center_y = (upper_no_rotate_t[1] + upper_no_rotate_t[5]) / 2.0

            upper_t[0] = (upper_no_rotate_t[0] - center_x) * math.cos(z_angle * math.pi / 360.0) - (upper_no_rotate_t[1] - center_y) * math.sin(z_angle * math.pi / 360.0) + center_x
            upper_t[1] = (upper_no_rotate_t[0] - center_x) * math.sin(z_angle * math.pi / 360.0) + (upper_no_rotate_t[1] - center_y) * math.cos(z_angle * math.pi / 360.0) + center_y
            upper_t[2] = (upper_no_rotate_t[2] - center_x) * math.cos(z_angle * math.pi / 360.0) - (upper_no_rotate_t[3] - center_y) * math.sin(z_angle * math.pi / 360.0) + center_x
            upper_t[3] = (upper_no_rotate_t[2] - center_x) * math.sin(z_angle * math.pi / 360.0) + (upper_no_rotate_t[3] - center_y) * math.cos(z_angle * math.pi / 360.0) + center_y
            upper_t[4] = (upper_no_rotate_t[4] - center_x) * math.cos(z_angle * math.pi / 360.0) - (upper_no_rotate_t[5] - center_y) * math.sin(z_angle * math.pi / 360.0) + center_x
            upper_t[5] = (upper_no_rotate_t[4] - center_x) * math.sin(z_angle * math.pi / 360.0) + (upper_no_rotate_t[5] - center_y) * math.cos(z_angle * math.pi / 360.0) + center_y
            upper_t[6] = (upper_no_rotate_t[6] - center_x) * math.cos(z_angle * math.pi / 360.0) - (upper_no_rotate_t[7] - center_y) * math.sin(z_angle * math.pi / 360.0) + center_x
            upper_t[7] = (upper_no_rotate_t[6] - center_x) * math.sin(z_angle * math.pi / 360.0) + (upper_no_rotate_t[7] - center_y) * math.cos(z_angle * math.pi / 360.0) + center_y

        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), upper_t)
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), textureCoordinates)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        # 画背景脸--指定区域不动
        glUniform1f(self.gl_draw_change_param_A, 1.0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, in_tex)
        glUniform1i(self.gl_draw_change_param_SamplerRGB, 1)

        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 0, cur_face_vertex_pos)
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 0, cur_face_texture_pos)

        glDrawElements(GL_TRIANGLES, self.ALL_TRIANGELS_NUM * 3, GL_UNSIGNED_SHORT, self.allIndices)

        # 画脸部表情
        glUniform1f(self.gl_draw_change_param_A, 1.0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, in_tex)
        glUniform1i(self.gl_draw_change_param_SamplerRGB, 1)
        glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 0, cur_face_vertex_pos)
        glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 0, cur_face_texture_pos)
        glDrawElements(GL_TRIANGLES, self.FACE_TRIANGLES_NUM * 3, GL_UNSIGNED_SHORT, self.faceIndices)
        # glVertexAttribPointer(ATTRIB_VX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), vertices)
        # glVertexAttribPointer(ATTRIB_TEX, 2, GL_FLOAT, 0, 2 * sizeof(GLfloat), textureCoordinates)
        # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glDisableVertexAttribArray(ATTRIB_VX)
        glDisableVertexAttribArray(ATTRIB_TEX)


        glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)

        return out_tex


    def gl_draw_context_uninit(self):
        if self.uninit_flag:
            return

        if self.gl_draw_texture_program:
            glDeleteProgram(self.gl_draw_texture_program)

        if self.gl_draw_change_program:
            glDeleteProgram(self.gl_draw_change_program)

        if self.gl_draw_flip_y_program:
            glDeleteProgram(self.gl_draw_flip_y_program)


        if self.src_tex  :
            glDeleteTextures( self.src_tex)

        if self.rgba_tex :
            glDeleteTextures( self.rgba_tex)

        if self.draw_src_tex  :
            glDeleteTextures( self.draw_src_tex)

        if self.draw_rgba_tex  :
            glDeleteTextures( self.draw_rgba_tex)

        if self.mouth_tex :
            glDeleteTextures( self.mouth_tex)

        if self.tongue_tex :
            glDeleteTextures( self.tongue_tex)

        self.uninit_flag = True

    def __del__(self):
        #self.gl_draw_context_uninit()
        pass
