#coding=utf-8

# error code
ERROR_INTERNAL_ERROR = 1
ERROR_NO_FACE = 2
ERROR_PARAM = 3
ERROR_DOWNLOAD = 4
ERROR_UPLOAD = 5

code_str = {
    ERROR_INTERNAL_ERROR: 'internal error',
    ERROR_NO_FACE: 'no face detected',
}

def error_code_str(code):
    if code not in code_str:
        code = ERROR_INTERNAL_ERROR

    return code_str[code]

class NoFaceDetected(Exception):
    pass