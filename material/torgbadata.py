import numpy as np
import cv2

img = cv2.imread('teeth.png',cv2.IMREAD_UNCHANGED)
img.tofile('teeth.rgba')