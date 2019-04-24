from processing.component.node_ftp_upload import  FtpUpload

if __name__ == '__main__':
    node = FtpUpload()
    node.params = {}
    node.params['video_id'] = '90367798'
    node.params['video_output'] = '1000.mp4'

    print(node.init())
    print(node.do())