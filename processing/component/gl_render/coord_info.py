# coding=utf-8
import cv2
import numpy as np

class FaceInfo():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.face_count = 1
        self.faces = []
        self.rgba = None

class Material():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.data = None

class Teeth(Material):
    pass

class Tongue(Material):
    pass



class FrameInfo():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.frames = []

    def set_material(self):
        teeth_path = './material/teeth.png'
        tongue_path =  './material/tongue.png'

        self.teeth = Teeth()
        self.teeth.data = cv2.cvtColor( cv2.imread(teeth_path,cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        self.teeth.width = self.teeth.data.shape[1]
        self.teeth.height = self.teeth.data.shape[0]

        self.tongue = Tongue()
        self.tongue.data = cv2.cvtColor( cv2.imread(tongue_path,cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        self.tongue.width = self.tongue.data.shape[1]
        self.tongue.height = self.tongue.data.shape[0]

