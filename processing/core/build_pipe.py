# coding=utf-8

from .pipe import Pipe
from .sub_pipe import SubPipe
# from pipe_node import PipeNode, Filter


def build_test_pipe(params):

    from ..component.filter_input_one_pic import InputOnePic
    from ..component.filter_gl_render import GLRenderFilter
    from ..component.filter_encode_video import EncodeVideo

    new_pipe = Pipe()
    new_pipe.params = params
    new_sub_pipe = SubPipe()
    new_pipe.add_sub_pipe(new_sub_pipe) # before sub pipe add filter

    new_sub_pipe.add_filter(InputOnePic())
    new_sub_pipe.add_filter(GLRenderFilter())
    new_sub_pipe.add_filter(EncodeVideo())

    new_pipe.init()

    return new_pipe

def build_test2_pipe(params):
    from ..component.filter_input_one_pic import InputOnePic
    from ..component.filter_gl_render import GLRenderFilter
    from ..component.filter_fake_render import FakeRenderFilter
    from ..component.filter_encode_video import EncodeVideo
    from ..component.node_prepare_face_trans import PrepareFaceTrans
    from ..component.node_ftp_upload import FtpUpload
    from ..component.node_face_report import FaceReport
    from ..component.node_woker_logging import WorkerLogging

    new_pipe = Pipe()
    new_pipe.params = params

    new_pipe.add_begin_node(PrepareFaceTrans())
    new_pipe.add_begin_node(WorkerLogging())

    new_pipe.add_super_finish_node(FaceReport())

    new_sub_pipe = SubPipe()
    new_pipe.add_sub_pipe(new_sub_pipe)  # before sub pipe add filter

    new_sub_pipe.add_filter(InputOnePic())
    new_sub_pipe.add_filter(GLRenderFilter())
    # new_sub_pipe.add_filter(FakeRenderFilter())
    new_sub_pipe.add_filter(EncodeVideo())

    new_pipe.init()

    return new_pipe

def build_face_trans_pipe(params):
    from ..component.filter_input_one_pic import InputOnePic
    from ..component.filter_gl_render import GLRenderFilter
    #from ..component.filter_fake_render import FakeRenderFilter
    from ..component.filter_encode_video import EncodeVideo
    from ..component.node_prepare_face_trans import PrepareFaceTrans
    from ..component.node_ftp_upload import FtpUpload
    from ..component.node_face_report import FaceReport
    from ..component.node_woker_logging import WorkerLogging

    new_pipe = Pipe()
    new_pipe.params = params

    new_pipe.add_begin_node(PrepareFaceTrans())
    new_pipe.add_begin_node(WorkerLogging())

    new_pipe.add_finish_node(FtpUpload())

    new_pipe.add_super_finish_node(FaceReport())

    new_sub_pipe = SubPipe()
    new_pipe.add_sub_pipe(new_sub_pipe)  # before sub pipe add filter

    new_sub_pipe.add_filter(InputOnePic())
    new_sub_pipe.add_filter(GLRenderFilter())
    # new_sub_pipe.add_filter(FakeRenderFilter())
    new_sub_pipe.add_filter(EncodeVideo())

    new_pipe.init()

    return new_pipe


filter_map = {
    'test': build_test_pipe,
    'test2': build_test2_pipe,
    'face_trans': build_face_trans_pipe,
}

def build_pipe(type, params):
    handler = filter_map[type]
    return handler(params)