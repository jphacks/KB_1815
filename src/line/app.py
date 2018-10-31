import os
import requests
import json
from flask import Flask, request
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
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('channel_acces_token', None)
ADMIN_ID = os.getenv('ADMIN_ID', None)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

ENDPOINT = config_loader.load('./config/endpoint.yml')
IMAGE_FILES = config_loader.load('./config/images.yml')


HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer%s' % CHANNEL_ACCESS_TOKEN
}


@app.route("/button_on", methods=['POST'])
def button_on():
    # 写真を撮る
    # スピーカーが誰か尋ねる
    # マイクで音声から文字起こし
    snap_shot(ADMIN_ID)

@app.route("/who", methods=['POST'])
def who(body):
    print(body)
    # notification(body)
    return()

@app.route("/callback", methods=['POST'])
def callback():
    global hatsuwa_flag
    response = request.get_json()
    events = response.get("events")

    for i in events:
        ID = i.get("source")["userId"]
        types = i.get("type")

        if(types == "message"):
            h = i.get("message")
            text = h["text"]

            if True in (x in text for x in ["開"]):
                    ask_open_key()

            elif True in (x in text for x in ["施錠", "閉"]):
                    ask_close_key()
            elif (text == "対話スイッチ"):
                    talkmode_switch()

            elif (text == "スナップショット"):
                    print(snap_shot(ID))

            elif (text == "決済"):
                post2one('https://733bc45e.ngrok.io/reserve', ID)

            elif hatsuwa_flag:
                if (text == "対話モードオフ"):
                    talkmode_switch()
                else:
                    post2one(text+" と伝えたよ", ID)
            else:
                if(text == "ピンポン"):
                    # 写真を撮る
                    # スピーカーが誰か尋ねる
                    # マイクで音声から文字起こし
                    postimage(IMAGE_FILES['HORN'], ID)
                    print(notification("佐川男子"))  # 宿主に電話対応するか尋ねる
                elif (text == "対話モードオフ"):
                    talkmode_switch()
                else:
                    post2one("意味がわかりません", ID)
                    poststamp(11537, 52002756, ID)

        elif(types == "postback"):
            h = i.get("postback")
            data = h["data"]

            if(data == "connect video"):
                post2one("video start", ID)

            elif(data == "ask talkmode"):
                print("ask_talkmode")
                ask_talkmode()

            elif(data == "ask requirements"):
                print("要件を訪ねます")
                post2one("要件を訪ねます", ID)

            elif(data == "open key"):
                print("開錠します")
                open_key()
                post2one("開錠します", ID)

            elif(data == "close key"):
                print("施錠します")
                close_key()
                post2one("施錠します", ID)

            elif(data == "keep key"):
                print("取りやめました")
                post2one("取りやめました", ID)

            elif(data == "talkmode on"):
                post2one("対話モード開始", ID)
                poststamp(11537, 52002741, ID)
                hatsuwa_flag = True
                template_response(ID)

            elif(data == "talkmode off"):
                post2one("対話モード終了", ID)
                poststamp(11537, 52002771, ID)
                hatsuwa_flag = False

            elif(data == "bye"):
                post2one("要件だけ聞いておきますね", ID)
                poststamp(11537, 52002750, ID)

        elif(types == "beacon"):
            h = i.get("beacon")
            action = h["type"]
            beacon_action(action, ID)
        elif(types == "follow"):
            print("thanks follw")
            send_first_message(ID)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

def beacon_action(action, ID):
    if(action == "enter"):
        print("becon,enter")
        post2admin("誰か帰ってきたよ")
    else:
        None

def poststamp(a, b, ID):
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

def postimage(image_url, ID):
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
        ENDPOINT['POSTIMAGE'],
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
        ENDPOINT['POST2ONE'],
        headers=HEADER,
        data=json.dumps(data),
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
        ENDPOINT['POST2OTHERS'],
        headers=HEADER,
        data=json.dumps(data),
    )

def notification(name, ID=ADMIN_ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "ボタンが押された時のテンプレート",
                "template": {
                    "type": "buttons",
                    "text": name + "さんが来客です。現在、電話対応可能ですか？",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "Yes",
                            "data": "connect video",
                        },
                        {
                            "type": "postback",
                            "label": "No",
                            "data": "ask talkmode",
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


def ask_close_key():
    data = {
        "to": ADMIN_ID,
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

def ask_talkmode():
    data = {
        "to": ADMIN_ID,
        "messages": [
            {
                "type": "template",
                "altText": "対話モードの確認",
                "template": {
                    "type": "buttons",
                    "text": "LINEで対応可能ですか？",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "Yes",
                            "data": "talkmode on",
                        },
                        {
                            "type": "postback",
                            "label": "No",
                            "data": "bye",
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

def ask_open_key():
    data = {
        "to": ADMIN_ID,
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
    response = requests.post(ENDPOINT['OPEN_KEY'])

    return(response)

def close_key():
    response = requests.post(ENDPOINT['OPEN_KEY'])

    return(response)

def send_first_message(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "This is a buttons template",
                "template": {
                    "type": "buttons",
                    "thumbnailImageUrl": "https://matsuko.link/img/intro_01.jpg",
                    "imageAspectRatio": "square",
                    "imageSize": "cover",
                    "imageBackgroundColor": "#FFFFFF",
                    "title": "初めまして、あなたはだれ？",
                    "text": "選んで下さい",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "ママ",
                            "data": "%s:ママ" % ID,
                            "text": "ママだよ"
                        },
                        {
                            "type": "postback",
                            "label": "パパ",
                            "data": "%s:パパ" % ID,
                            "text": "パパだよ"
                        },
                        {
                            "type": "postback",
                            "label": "太郎",
                            "data": "%s:太郎" % ID,
                            "text": "太郎だよ"
                        },
                        {
                            "type": "postback",
                            "label": "花子",
                            "data": "%s:花子" % ID,
                            "text": "花子だよ"
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


def template_response(ID):
    data = {
        "to": ID,
        "messages": [
            {
                "type": "template",
                "altText": "定型返答用のカルーセルテンプレート",
                "template": {
                    "type": "carousel",
                    "columns": [
                        {
                            "thumbnailImageUrl": IMAGE_FILES['TEMPLATE_RESPONSE'],
                            "imageBackgroundColor": "#FFFFFF",
                            "title": "質問",
                            "text": "訪問者に質問します",
                            "defaultAction": {
                                "type": "uri",
                                "label": "View detail",
                                "uri": "http://example.com/page/123"
                            },
                            "actions": [
                                {
                                    "type": "postback",
                                    "label": "要件はなんですか？",
                                    "data": "要件はなんですか？",
                                    "text": "要件はなんですか？"
                                },
                                {
                                    "type": "postback",
                                    "label": "誰にご用ですか？",
                                    "data": "誰にご用ですか？",
                                    "text": "誰にご用ですか？"
                                },
                            ]
                        },
                        {
                            "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
                            "imageBackgroundColor": "#FFFFFF",
                            "title": "お礼、謝罪",
                            "text": "お礼をしたり、謝ったり",
                            "defaultAction": {
                                "type": "uri",
                                "label": "View detail",
                                "uri": "http://example.com/page/123"
                            },
                            "actions": [
                                {
                                    "type": "postback",
                                    "label": "ありがとう",
                                    "data": "ありがとう",
                                    "text": "ありがとう"
                                },
                                {
                                    "type": "postback",
                                    "label": "ごめんなさい",
                                    "data": "ごめんなさい",
                                    "text": "ごめんなさい"
                                },
                            ]
                        },
                        {
                            "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
                            "imageBackgroundColor": "#FFFFFF",
                            "title": "在宅時間を通知",
                            "text": "だいたい、いつ帰る？？",
                            "defaultAction": {
                                "type": "uri",
                                "label": "View detail",
                                "uri": "http://example.com/page/123"
                            },
                            "actions": [
                                {
                                    "type": "postback",
                                    "label": "夜には帰ります",
                                    "data": "夜には帰ります",
                                    "text": "夜には帰ります"
                                },
                                {
                                    "type": "postback",
                                    "label": "今日は帰りません",
                                    "data": "今日は帰りません",
                                    "text": "今日は帰りません"
                                },
                            ]
                        }
                    ],
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

def snap_shot(ID):
    response = requests.get(ENDPOINT['SNAP_SHOT'])
    postimage(IMAGE_FILES['SNAP_SHOT'], ID)
    return(response)

def LINE_PAY():
    response = requests.get(ENDPOINT['LINE_PAY'])
    return(response)


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
