from south_east_asia.uploader import uploadVideo as seaUploadVideo
from us.uploader import uploadVideo as usUploadVideo
from deta import Deta
import time
import requests
import json
import os
import time

deta = Deta("c0cgqjui_JYrRnnJL9539GXuwFAW59RsfMUgCL5Cd")
to_upload = deta.Base('service_tk_upload')


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
            "发布状态": "%s" %result
            
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




def get_download_link(file_token):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url?file_tokens=%s" %file_token
    payload = ''


    headers = {
    'Authorization': 'Bearer %s' %get_token()
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    if response['code'] == 0:
        return response['data']['tmp_download_urls'][0]['tmp_download_url']
    else:
        return ''
    

def download_video(video_link):
    try:
        with requests.get(video_link) as r:
            with open(r'C:\Users\Administrator\Desktop\TikTokUploder\temp.mp4', 'wb') as o:
                o.write(r.content)
    except Exception as e:
        print(e, '下载失败')
        
        download_video(video_link)

def _now():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def upload_tasks():
    tasks = to_upload.fetch().items
    if len(tasks)>0:
        for task in tasks:
            session_id = task['session_id'][0]['text']
            video_token = task['视频'][0]['file_token']
            video_url = get_download_link(video_token)
            download_video(video_url)
            video_path = os.path.join( r'C:\Users\Administrator\Desktop\TikTokUploder', 'temp.mp4' )   
            title = task['标题']
            tags = task['标签（#开头，空格间隔）']
            status = False
            if task['账号国家'][0] == 'optrH7Iyyz':  #如果是美国账号
                try:
                    status = usUploadVideo(session_id, video_path, title, tags)
                except Exception as e:
                    
                    
                    print(e, '上传失败', _now())
                    upload_feedback(task, '失败')
        # session_id = 'c69bd7c225128f0b52e17e4d7b9adaaf'
        # video_path = '/Users/nobody1/Downloads/final_video.mp4'
        # title = 'Đồ chơi trẻ em thú vị'
        # tags = '#Đồ chơi'
            else:  #否则按东南亚国家处理
                try:
                    status = seaUploadVideo(session_id, video_path, title, tags)
                except Exception as e:
                    print(e, '上传失败', _now())
                    upload_feedback(task, '失败')

            if status:
                print('上传成功', _now())
                to_upload.delete(task['key'])
                upload_feedback(task, '已上')
            else:
                print('上传失败', _now())
                # to_upload.delete(task['key'])
                upload_feedback(task, '失败')

    else:
        print('没有视频要上传', _now())
        time.sleep(1200)
        


if __name__ == "__main__":
    upload_tasks()