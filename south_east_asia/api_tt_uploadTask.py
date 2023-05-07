from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta
from tt_upload import get_token
import requests



app = FastAPI()
deta = Deta("c0cgqjui_JYrRnnJL9539GXuwFAW59RsfMUgCL5Cd")
tk_upload = deta.Base('tk_upload')

# 80端口对外开放

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_row_data(record_id):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/bascnkKSvx583V9CBpQ3rOEKcUf/tables/tblZB3mSz2zYnWTp/records/%s" %record_id
    payload = ''

    headers = {
    'Authorization': 'Bearer %s' %get_token()
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response['data']['fields']



@app.get('/tt_upload/record_id={record_id}')
async def tt_to_deta(record_id: str):
    """接口从飞书输入图片的file_token和record_id，获取图片链接，下载图片，用背景图生成新图片，上传新图片"""
    print(record_id)
    to_deta = get_row_data(record_id)
    to_deta['record_id'] = record_id
    tk_upload.put(to_deta)

    return record_id
