# -*- coding: utf-8 -*-

import urllib.parse
import os
import sys
import requests,json
from argparse import ArgumentParser
from userlist import user_list
import random
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)

hatsuwa_flag = False

channel_secret = os.environ["channel_secret"]
channel_access_token = os.environ["channel_acces_token"]
admin_ID = os.environ['admin_ID']
print(admin_ID)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/button_on", methods=['POST'])
def button_on():
    #写真を撮る
    #スピーカーが誰か尋ねる
    #マイクで音声から文字起こし
    postimage("https://shop.r10s.jp/book/cabinet/4798/4900459524798_2.jpg",admin_ID)
    bottan_on("佐川男子") #宿主に電話対応するか尋ねる


@app.route("/callback", methods=['POST'])
def callback():
    global hatsuwa_flag
    body = request.get_json()
    body2 = body.get("events")
    
    for i in body2:
        ID= i.get("source")["userId"]
        types = i.get("type")
        
        if(types=="message"):
            h = i.get("message")
            text = h["text"]
            
            if True in (x in text  for x in ["開"]):
                    ask_open_key()
                
            elif True in (x in text  for x in ["施錠","閉"]):
                    ask_close_key()
            
            elif hatsuwa_flag:
                if (text=="対話モードオフ"):
                    talkmode_switch()
                else:
                    post2one(text+" と伝えたよ",ID)
            else:
                if(text == "ピンポン"):
                    #写真を撮る
                    #スピーカーが誰か尋ねる
                    #マイクで音声から文字起こし
                    postimage("https://shop.r10s.jp/book/cabinet/4798/4900459524798_2.jpg",ID)
                    #postimage("https://80f71b17.ngrok.io/image.jpg",ID)
                    print(bottan_on("佐川男子")) #宿主に電話対応するか尋ねる
                elif (text=="対話モードオフ"):
                    talkmode_swith()
                else:
                    post2one("意味がわかりません",ID)
                    poststamp(11537,52002756,ID)

        elif(types=="postback"):
            h = i.get("postback")
            data = h["data"]

            if(data == "connect video"):
                post2one("video start",ID)
            
            elif(data == "ask talkmode"):
                print("ask_talkmode")
                ask_talkmode()
           
            elif(data == "ask requirements"):
                print("要件を訪ねます")
                post2one("要件を訪ねます",ID)
            
            elif(data == "open key"):
                print("開錠します")
                open_key()
                post2one("開錠します",ID)
            
            elif(data == "close key"):
                print("施錠します")
                close_key()
                post2one("施錠します",ID)
            
            elif(data == "keep key"):
                print("取りやめました")
                post2one("取りやめました",ID)
            
            elif(data == "talkmode on"):
                post2one("対話モード開始",ID)
                poststamp(11537,52002741,ID)
                hatsuwa_flag = True
                template_response(ID)
            
            elif(data == "talkmode off"):
                post2one("対話モード終了",ID)
                poststamp(11537,52002771,ID)
                hatsuwa_flag = False

            elif(data == "bye"):
                post2one("要件だけ聞いておきますね",ID)
                poststamp(11537,52002750,ID)

        elif(types=="beacon"):
            h = i.get("beacon")
            action = h["type"]
            beacon_action(action,ID)
        elif(types=="follow"):
            print("thanks follw")
            send_first_message(ID)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

def beacon_action(action,ID):
    if(action=="enter"):
        print("becon,enter")
        post2admin("誰か帰ってきたよ")
    else:
        None

def poststamp(a,b,ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
            {
                "type":'sticker',
                'packageId' : a,
                'stickerId' : b,
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    
    requests.post(url, data=json.dumps(data), headers=headers)

def okaeri(ID):
    post_image = "https://matsuko.link/img/okaeri.jpg"
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
            {
                "type": "image",
                "originalContentUrl" : post_image,
                "previewImageUrl":post_image,
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }

    requests.post(url, data=json.dumps(data), headers=headers)

def postimage(post_image,ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
            {
                "type": "image",
                "originalContentUrl" : post_image,
                "previewImageUrl":post_image,
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    
    requests.post(url, data=json.dumps(data), headers=headers)

def post2admin(post_text):
    print(admin_ID)
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":admin_ID,
        "messages":[
            {
                "type": "text",
                "text": post_text 
            }
        ]
    }
    print(post_text)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def post2one(post_text, ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
            {
                "type": "text",
                "text": post_text 
            }
        ]
    }
    print(post_text)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def post2others(post_text, ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
            {
                "type": "text",
                "text": post_text 
            }
        ]
    }

    print(post_text)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }

    requests.post(url, data=json.dumps(data), headers=headers)

def bottan_on(name,ID=admin_ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":ID,
        "messages":[
        {
            "type": "template",
            "altText": "ボタンが押された時のテンプレート",
            "template": {
                "type": "buttons",
                "text":  name + "さんが来客です。現在、電話対応可能ですか？",
                "actions": [
                    {
                      "type": "postback",
                      "label":"Yes",
                      "data" : "connect video",
                    },
                    {
                      "type": "postback",
                      "label":"No",
                      "data": "ask talkmode",
                    }
                ]
            }
}
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)
    

def ask_close_key():
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":admin_ID,
        "messages":[
        {
            "type": "template",
            "altText": "施錠時のテンプレート",
            "template": {
                "type": "buttons",
                "text":  "施錠しますか？",
                "actions": [
                    {
                      "type": "postback",
                      "label":"Yes",
                      "data" : "close key",
                    },
                    {
                      "type": "postback",
                      "label":"No",
                      "data": "keep key",
                    }
                ]
            }
}
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def talkmode_switch():
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":admin_ID,
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
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def ask_talkmode():
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":admin_ID,
        "messages":[
        {
            "type": "template",
            "altText": "対話モードの確認",
            "template": {
                "type": "buttons",
                "text":  "LINEで対応可能ですか？",
                "actions": [
                    {
                      "type": "postback",
                      "label":"Yes",
                      "data" : "talkmode on",
                    },
                    {
                      "type": "postback",
                      "label":"No",
                      "data": "bye",
                    }
                ]
            }
}
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)
def ask_open_key():
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to":admin_ID,
        "messages":[
        {
            "type": "template",
            "altText": "開錠時のテンプレート",
            "template": {
                "type": "buttons",
                "text":  "開錠しますか？",
                "actions": [
                    {
                      "type": "postback",
                      "label":"Yes",
                      "data" : "open key",
                    },
                    {
                      "type": "postback",
                      "label":"No",
                      "data": "keep key",
                    }
                ]
            }
}
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def open_key():
    response = requests.post('http://ea158e60.ngrok.io/open', )
    return(response)

def close_key():
    response = requests.post('http://ea158e60.ngrok.io/close', )
    return(response)

def send_first_message(ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
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
                      "label":"ママ",
                      "data":ID+":ママ",
                      "text":"ママだよ"
                    },
                    {
                      "type": "postback",
                      "label":"パパ",
                      "data":ID+":パパ",
                      "text":"パパだよ"
                    },
                    {
                      "type": "postback",
                      "label":"太郎",
                      "data":ID+":太郎",
                      "text":"太郎だよ"
                    },
                    {
                      "type": "postback",
                      "label":"花子",
                      "data":ID+":花子",
                      "text":"花子だよ"
                    }
                ]
            }
        }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)


def template_response(ID):
    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": ID,
        "messages":[
        {
            "type": "template",
            "altText": "定型返答用のカルーセルテンプレート",
            "template": {
                "type": "carousel",
                "columns": [
                    {
                      "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
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
                              "text":"要件はなんですか？"
                          },
                          {
                              "type": "postback",
                              "label": "誰にご用ですか？",
                              "data": "誰にご用ですか？",
                              "text":"誰にご用ですか？"
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
                              "text":"ありがとう"
                          },
                          {
                              "type": "postback",
                              "label": "ごめんなさい",
                              "data": "ごめんなさい",
                              "text":"ごめんなさい"
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
                              "text":"夜には帰ります"
                          },
                          {
                              "type": "postback",
                              "label": "今日は帰りません",
                              "data": "今日は帰りません",
                              "text":"今日は帰りません"
                          },
                      ]
                    }#,
                ],
                "imageAspectRatio": "rectangle",
                "imageSize": "cover"
            }
    }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token 
    }
    requests.post(url, data=json.dumps(data), headers=headers)

if __name__ == "__main__":  
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
