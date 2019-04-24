#coding=utf-8

from ..core.pipe_node import PipeNode
from ..processing_exception import *
import random, string
import requests
from ftplib import FTP
import logging
import datetime
import traceback

def gen_rand_str(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt

class FtpUpload(PipeNode):
    def __init__(self):
        super(FtpUpload, self).__init__()
        self.ftp_query_url = 'http://your.server.com/outapi/ftp/getFtpServerIp2.do?from=3'
        self.ftp_ip = None
        self.ftp_usr = 'ftpvideo'
        self.ftp_passwd = 'password'

    def init(self):
        try:
            response = requests.get(self.ftp_query_url, headers={'Connection': 'close'})
            response.raise_for_status()

            data = response.json()

            if data['status'] != 1:
                self.error(ERROR_UPLOAD,'cant get ftp ip')
                return False

            self.ftp_ip = data['ftpIP']['masterIP']
            logging.info('ftp ip: %s', self.ftp_ip)

        except Exception as e:
            logging.error('ftp upload init: %s' % traceback.format_exc())
            self.error(ERROR_UPLOAD, 'error %s'%str(e))
            return False

        return True

    def gen_file_name(self, vid):
        date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        name = '_'.join(['fast1',vid,date,gen_rand_str(11)])
        name += '.mp4.600'
        return name

    def ftp_connect(self):
        ftp = FTP()
        # ftp.set_debuglevel(2)
        ftp.connect(self.ftp_ip, 21)
        # ftp.connect('10.11.134.20', 21) # test ftp server
        ftp.login(self.ftp_usr, self.ftp_passwd)
        return ftp

    def do(self):
        try:
            file_path = self.params['video_output']
            video_id = self.params['video_id']

            filename = self.gen_file_name(video_id)
            logging.info('upload file name %s',filename)

            filename_tmp = filename + '.tmp'
            ftp = self.ftp_connect()
            ftp.storbinary("STOR " + filename_tmp, open(file_path, 'rb'))

            filename_moved = filename + '.moved'
            ftp.rename(filename_tmp, filename_moved)
        except Exception as e:
            logging.error('ftp upload work: %s' % traceback.format_exc())
            self.error(ERROR_UPLOAD, 'error %s' % str(e))
            return False

        return True
