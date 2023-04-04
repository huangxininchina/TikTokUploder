from uploader import uploadVideo
from deta import Deta
import time


deta = Deta("c0cgqjui_JYrRnnJL9539GXuwFAW59RsfMUgCL5Cd")
to_upload = deta.Base('tt_upload')

def upload_tasks():
    tasks = to_upload.fetch().items
    if len(tasks)>0:
        for task in tasks:
            session_id = task['session_id']
            video_path = task['video_path']
            title = task['title']
            tags = task['tags']
        # session_id = 'c69bd7c225128f0b52e17e4d7b9adaaf'
        # video_path = '/Users/nobody1/Downloads/final_video.mp4'
        # title = 'Đồ chơi trẻ em thú vị'
        # tags = '#Đồ chơi'

            uploadVideo(session_id, video_path, title, tags)
    else:
        print('没有视频要上传')
        time.sleep(1200)
        


if __name__ == "__main__":
    upload_tasks()