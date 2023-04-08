from uploader import uploadVideo
from deta import Deta
import time
import requests
import json

deta = Deta("c0cgqjui_JYrRnnJL9539GXuwFAW59RsfMUgCL5Cd")
to_upload = deta.Base('tk_upload')


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": "cli_a49ac05c8a78500c",
        "app_secret": "8A17i1k4frBSWsHpnCI1gbYZNVSQlxhc"
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['tenant_access_token']




def upload_feedback(raw_data, result):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/bascnkKSvx583V9CBpQ3rOEKcUf/tables/tblZB3mSz2zYnWTp/records/%s" %raw_data['record_id']
    payload = json.dumps({
        "fields": {
            "发布状态": [
                "%s" %result
            ]
        }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' %get_token()
    }

    response = requests.request("PUT", url, headers=headers, data=payload).json()
    if response['code'] == 0:
        print(raw_data['record_id'], '已同步飞书')
    else:
        print(raw_data['record_id'], '同步飞书失败', response)





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

            status = uploadVideo(session_id, video_path, title, tags)
            if status:
                print('上传成功')
                to_upload.delete(task['key'])
                upload_feedback(task, '已上')
            else:
                print('上传失败')
                to_upload.delete(task['key'])
                upload_feedback(task, '失败')

    else:
        print('没有视频要上传')
        time.sleep(1200)
        


if __name__ == "__main__":
    upload_tasks()