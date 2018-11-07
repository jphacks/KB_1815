import time 
import os
import requests
import json
from flask import Flask, request,jsonify
from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from util import config_loader

app = Flask(__name__)

hatsuwa_flag = False
login_flag = False
registration_flag = False

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
PASSWORD = os.getenv('PASSWORD')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

ENDPOINT = config_loader.load('./config/endpoint.yml')
IMAGE_FILES = config_loader.load('./config/images.yml')
TALK_TEMPLETE = config_loader.load('./config/talk_templete.yml')
PASSWORD_TEMPLETE = config_loader.load('./config/password.yml')
LOGIN = config_loader.load('./config/login.yml')
PASS_SUCCESS = config_loader.load('./config/pass_success.yml')
CLOVA_RES = config_loader.load('./config/clova_res.yml')
TEMPLETE = config_loader.load('./config/templete.yml')

USER_LIST = config_loader.load('./config/user_list.yml')

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % CHANNEL_ACCESS_TOKEN
}
def login(passwd,ID):
    if passwd == PASSWORD:
        post2one(LOGIN['LOGIN_SUCCESS'],ID)
        PASS_SUCCESS[ID] = ""
        config_loader.dump(PASS_SUCCESS,'config/pass_success.yml')
        return(True)
    else:
        post2one(LOGIN['LOGIN_FALSE'],ID)
        return(False)

def registration(name,ID):
    USER_LIST[ID] = name
    print(USER_LIST)
    config_loader.dump(USER_LIST,'config/user_list.yml')
    post2one(name + 'で登録しました',ID)
    post2admin(ID + 'を' + name + 'という名前で登録しました')
    return(True)

def overwride(before,after):
    datas = {'before':before,
            'after':after}
    requests.post(
        ENDPOINT['RASPI2'] + '/sound',
        data=datas,
    )
    return() 

def beacon_action(action, ID):
    if(action == "enter"):
        print("becon,enter")
        if(ID in USER_ID):
            name = USER_ID[ID]
            # to ADMIN
            post2admin(name + "が帰宅しました")
            post2stamp('11537','52002741')
            # to YOUSER
            post2one("おかえりなさい、待ってたよ！！", ID)
            post2stamp('11537','52002736',ID)

    else:
        print("becon,leave")
        if(ID in USER_LIST):
            name = USER_LIST[ID]
            # to ADMIN
            post2admin(name + "がおでかけみたいです")
            post2stamp('11537','52002741')
            # to YOUSER
            post2one("行ってらっしゃい！良い1日になりますように", ID)
            poststamp('11537','52002736',ID)

def poststamp(a, b, ID = ADMIN_ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": 'sticker',
                'packageId': a,
                'stickerId': b,
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def okaeri(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": IMAGE_FILES['OKAERI'],
                "previewImageUrl": IMAGE_FILES['OKAERI'],
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def postimage2one(image_url, ID = ADMIN_ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url,
            }
        ]
    }

    requests.post(
        ENDPOINT['POST'],
        data=json.dumps(data),
        headers=HEADER,
    )

def post2admin(post_text):
    print(ADMIN_ID)
    data = {
        "to": ADMIN_ID,
        "messages": [
            {
                "type": "text",
                "text": post_text
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def post2one(post_text, ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "text",
                "text": post_text
            }
        ]
    }

    requests.post(
        ENDPOINT['POST'],
        data=json.dumps(data),
        headers=HEADER,
    )

def post2others(post_text, ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "text",
                "text": post_text
            }
        ]
    }

    requests.post(
        ENDPOINT['POST'],
        headers=HEADER,
        data=json.dumps(data),
    )

def notification(name, ID=ADMIN_ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "来客じの最初の対応",
                "template": {
                    "type": "buttons",
                    "text": name + "さんが来客です。どのように対応されますか",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "電話をつなぐ",
                            "data": "line telephone call",
                        },
                        {
                            "type": "postback",
                            "label": "LINEで対応",
                            "data": "line talk",
                        },
                        {
                            "type": "postback",
                            "label": "対応不可",
                            "data": "impossible",
                        }
                    ]
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )


def ask_close_key(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "施錠時のテンプレート",
                "template": {
                    "type": "buttons",
                    "text": "施錠しますか？",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "Yes",
                            "data": "close key",
                        },
                        {
                            "type": "postback",
                            "label": "No",
                            "data": "keep key",
                        }
                    ]
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def talkmode_switch():
    data = {
        "to": ADMIN_ID,
        "messages": [
            {
                "type": "template",
                "altText": "対話モードの確認",
                "template": {
                    "type": "buttons",
                    "text": "対話モード",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "ON",
                            "data": "talkmode on",
                        },
                        {
                            "type": "postback",
                            "label": "OFF",
                            "data": "talkmode off",
                        }
                    ]
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def ask_open_key(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "開錠時のテンプレート",
                "template": {
                    "type": "buttons",
                    "text": "開錠しますか？",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "Yes",
                            "data": "open key",
                        },
                        {
                            "type": "postback",
                            "label": "No",
                            "data": "keep key",
                        }
                    ]
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def open_key():
    response = requests.post(ENDPOINT['RASPI2']+'/open')

    return(response)

def close_key():
    response = requests.post(ENDPOINT['RASPI2']+'/close')

    return(response)

def send_first_message(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "最初のメッセージ",
                "template": {
                    "type": "buttons",
                    "thumbnailImageUrl": "https://aaa.jpg",
                    "imageSize": "cover",
                    "imageBackgroundColor": "#FFFFFF",
                    "title": PASSWORD_TEMPLETE['TITLE'],
                    "text": PASSWORD_TEMPLETE['DESCRIPTION'],
                    "actions": [
                        {
                            "type": "postback",
                            "label": PASSWORD_TEMPLETE['TYPE' + str(num + 1)]['TEXT'],
                            "data": PASSWORD_TEMPLETE['TYPE' + str(num + 1)]['DATA'],
                        } for num in range(PASSWORD_TEMPLETE['LEN'])
                    ]
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )


def template_response(ID):
    columns = [
        {    
            "thumbnailImageUrl": IMAGE_FILES['TEMPLATE_RESPONSE'],
            "imageBackgroundColor": "#FFFFFF",
            "title": TALK_TEMPLETE['M' + str(num + 1)]['TITLE'],
            "text": TALK_TEMPLETE['M' + str(num + 1)]['DESCRIPTION'],
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": ENDPOINT['TEMPLETE']
            },
            "actions": [
                {
                    "type": "postback",
                    "label": TALK_TEMPLETE['M' + str(num + 1)]['TYPE' + str(m_num + 1)]['TEXT'],
                    "data": TALK_TEMPLETE['M' + str(num + 1)]['TYPE' + str(m_num + 1)]['DATA'],
                    "text": TALK_TEMPLETE['M' + str(num + 1)]['TYPE' + str(m_num + 1)]['TEXT']
                } for m_num in range(TALK_TEMPLETE['M' + str(num + 1)]['LEN'])
            ]
        } for num in range(TALK_TEMPLETE['MESSAGE_LEN'])
    ]

    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "返答定型文",
                "template": {
                    "type": "carousel",
                    "columns": columns,
                    "imageAspectRatio": "rectangle",
                    "imageSize": "cover"
                }
            }
        ]
    }

    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def snap_shot():
    response = requests.get(ENDPOINT['RASPI2'] + '/photo')
    return(response)

def LINE_PAY():
    response = requests.get(ENDPOINT['LINE_PAY'])
    return(response)

def complete_res():
   # action = [
   #     {
   #       "type": "postback",
   #       "label": TEMPLETE['COMPLETE']['LABEL' + str(num + 1)],
   #       "data": TEMPLETE['COMPLETE']['DATA' + str(num + 1)],
   #     } for num in range(TEMPLETE['COMPLETE']['LEN'])
   # ]
   # data = {
   #     "to":ADMIN_ID,
   #     "messages":[
   #     {
   #         "type": "template",
   #         "altText": "決済完了後のテンプレート",
   #         "template": {
   #             "type": "buttons",
   #             "text": TEMPLETE['COMPLETE']['TITLE'],
   #             "actions":action            
   #         }
   #     }
   #     ]
   # }
   # requests.post(
   #     ENDPOINT['PUSH_URL'],
   #     headers=HEADER,
   #     data=json.dumps(data),
   # )
   # print(TEMPLETE['COMPLETE'])
    data = {
        "to":ADMIN_ID,
        "messages":[
        {
            "type": "template",
            "altText": "受けトリ完了",
            "template": {
                "type": "buttons",
                "text":  "荷物のうけトリが完了しました。施錠しますか？",
                "actions": [
                    {
                      "type": "postback",
                      "label":"はい",
                      "data" : "close key",
                    },
                    {
                      "type": "postback",
                      "label":"いいえ",
                      "data": "no",
                    }
                ]
            }
        }
        ]
    }
    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )


def talkmode_switch():
    data = {
        "to":ADMIN_ID,
        "messages":[
        {
            "type": "template",
            "altText": "対話モードの確認",
            "template": {
                "type": "buttons",
                "text":  "対話モード",
                "actions": [
                    {
                      "type": "postback",
                      "label":"ON",
                      "data" : "talkmode on",
                    },
                    {
                      "type": "postback",
                      "label":"OFF",
                      "data": "talkmode off",
                    }
                ]
            }
        }
        ]
    }
    requests.post(
        ENDPOINT['PUSH_URL'],
        headers=HEADER,
        data=json.dumps(data),
    )

def qr2url(image_path):
    datas = {'image_path':str(image_path)}
    res = requests.post(
            ENDPOINT['QR2URL'],
            json.dumps(datas),
        )
    print(res)
    print(type(res))
    data = res.json()
    url = data['url']
    post2admin(url)

def call():
    print('call')
    response = requests.get(ENDPOINT['RASPI2']+'/call')
    return(response)

