from func import *


@app.route("/important", methods=['POST'])
def important():
    post2admin('重要な書類が届きました')
    data = request.data.decode('utf-8')
    data = json.loads(data)
    path = ENDPOINT['RASPI1'] + '/images/' + data['result']
    postimage2one(path)
    poststamp('11537','52002741')

@app.route("/who", methods=['POST'])
def who(body):
    print(body)
    # notification(body)
    return() 
@app.route("/callback", methods=['POST'])
def callback():
    global hatsuwa_flag
    global registration_flag
    global login_flag
    body = request.get_json()
    body2 = body.get("events")
    for i in body2:
        print(i)
        ID = i.get("source")["userId"]
        types = i.get("type")
        registration_flag = False
        login_flag = False

        if ID in USER_LIST:
            registration_flag = True
            login_flag = True
            
        elif ID in PASS_SUCCESS:
            registration_flag = False
            login_flag = True
    
        if(types == "beacon"):
            h = i.get("beacon")
            action = h["type"]
            beacon_action(action, ID)
        
        elif(types == "follow"):
            if ID in USER_LIST:
                print('おかえり')
                registration_flag = True
                login_flag = True
                name = USER_LIST[ID] 
                post2one(name + 'さん、お帰りなさいませ！',ID)
                poststamp('11537','52002736',ID)
            else:
                print('新規ユーザ')
                registration_flag = False
                login_flag = False
                send_first_message(ID)

        elif not(login_flag):
            try:
                if(types == "postback"):
                    h = i.get("postback")
                    data = h["data"]
                    if(data == PASSWORD_TEMPLETE['TYPE1']['DATA']): #'login'
                        post2one('pass:ここにパスワードを入力 の形式でパスワードを入力して下さい',ID)
                    elif(data == PASSWORD_TEMPLETE['TYPE2']['DATA']): #'no_password'
                        post2one(LOGIN['TO_ADMIN'],ID)
                        post2admin('登録希望(ID:' + ID + ')が届きました。心当たりがあればパスワードを教えてあげて下さい')
                else:
                    h = i.get("message")
                    text = h["text"]
                    if(text[0:5] == 'pass:'):
                        login_flag = login(text[5:],ID)
                    else:
                        post2one(LOGIN['PLESE_PASS'],ID)
                
            except:
                post2one(LOGIN['PLESE_PASS'],ID)

        elif not(registration_flag):
                try:
                    h = i.get("message")
                    text = h["text"]
                    print(text)
                    if(text[0:5] == 'name:'):
                        registration_flag = registration(text[5:],ID)
                    else:
                        post2one(LOGIN['PLESE_NAME'],ID)
                    
                except:
                    post2one(LOGIN['PLESE_NAME'],ID)
        else:
            if(types == "message"):
                h = i.get("message")
                text = h["text"]
        
                if True in (x in text for x in ["開"]):
                        ask_open_key(ID)
        
                elif True in (x in text for x in ["施錠", "閉"]):
                        ask_close_key(ID)
                elif (text == "対話スイッチ"):
                        talkmode_switch()
                
                elif (text == "電話をつないで"):
                        ask_call(ID)
        
                elif (text == "スナップショット"):
                        ask_snap_shot(ID)
        
                elif (text == "決済"):
                    post2one('https://733bc45e.ngrok.io/reserve', ID)
                elif hatsuwa_flag:
                    if (text=="対話モードオフ"):
                        talkmode_switch()
                else:
                    if(text in ['はい','いいえ']):
                        None

                    elif(text == "ピンポン"):
                        notification("佐川男子")
                    else:
                        post2one("意味がわかりません", ID)
                        poststamp(11537, 52002756, ID)
        
            elif(types == "postback"):
                h = i.get("postback")
                data = h["data"]
        
                if(data == TALK_TEMPLETE['M1']['TYPE1']['DATA']): #'ask_youken'
                    post2admin(TALK_TEMPLETE['M1']['TYPE1']['RET'])
                    overwride(TALK_TEMPLETE['M1']['TYPE1']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M1']['TYPE2']['DATA']): #'ask_who'
                    post2admin(TALK_TEMPLETE['M1']['TYPE2']['RET'])
                    overwride(TALK_TEMPLETE['M1']['TYPE2']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M2']['TYPE1']['DATA']): #'get_QR'
                    post2admin(TALK_TEMPLETE['M2']['TYPE1']['RET'])
                    poststamp(11537,52002736,ID)
                    overwride(TALK_TEMPLETE['M2']['TYPE1']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M2']['TYPE2']['DATA']): #'get_info'
                    post2admin(TALK_TEMPLETE['M2']['TYPE2']['RET'])
                    poststamp(11537,52002736,ID)
                    overwride(TALK_TEMPLETE['M2']['TYPE2']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M3']['TYPE1']['DATA']): #'complete_pay'
                    complete_pay()
                    poststamp(11537,52002741,ID)
                    overwride(TALK_TEMPLETE['M3']['TYPE1']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M3']['TYPE2']['DATA']): #'complete_info'
                    complete_info()
                    poststamp(11537,52002741,ID)
                    overwride(TALK_TEMPLETE['M3']['TYPE2']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M4']['TYPE1']['DATA']): #'thanks'
                    post2admin(TALK_TEMPLETE['M4']['TYPE1']['RET'])
                    poststamp(11537,52002741,ID)
                    overwride(TALK_TEMPLETE['M4']['TYPE1']['DATA'],'default')
                
                elif(data == TALK_TEMPLETE['M4']['TYPE2']['DATA']): #'every_thanks'
                    post2admin(TALK_TEMPLETE['M4']['TYPE2']['RET'])
                    poststamp(11537,52002741,ID)
                    overwride(TALK_TEMPLETE['M4']['TYPE2']['DATA'],'default')
        
                elif(data == "line telephone call"):
                    post2admin("LINE通話を開始します")
                    call(ID)
        
                elif(data == "line talk"):
                    post2admin("承知しました")
                    poststamp(11537, 52002741, ID)
                    template_response(ID)
                    hatsuwa_flag = True
                
                elif(data == "impossible"):
                    post2admin("要件だけ聞いておきますね")
                    poststamp(11537, 52002750, ID)
        
                elif(data == "ask requirements"):
                    print("要件を訪ねます")
                    post2one("要件を訪ねます", ID)
                
                elif(data == "start call"):
                    try:
                        call(ID)
                        post2one("通話を開始します", ID)
                    except:
                        post2one("通話に失敗しました", ID)
        
                elif(data == "snap shot"):
                    try:
                        send_snap_shot(ID)
                        post2one("撮影しました", ID)
                    except:
                        post2one("撮影に失敗しました", ID)
                
                elif(data == "uketori_open key"):
                    try:
                        open_key()
                        post2one("開錠しました", ID)
                        template_response(ID)
                    except:
                        post2one("開錠に失敗しました", ID)
                
                elif(data == "open key"):
                    try:
                        open_key()
                        post2one("開錠しました", ID)
                    except:
                        post2one("開錠に失敗しました", ID)

                elif(data == "complete close key"):
                    try:
                        close_key()
                        post2one("施錠しました", ID)
                        template_response(ID)
                    except:
                        post2one("施錠に失敗しました", ID)
        

                elif(data == "close key"):
                    try:
                        close_key()
                        post2one("施錠しました", ID)
                    except:
                        post2one("施錠に失敗しました", ID)
        
                elif(data == "keep key"):
                    print("取りやめました")
                    post2one("取りやめました", ID)

                elif(data == "talkmode on"):
                    post2one("対話モード開始",ID)
                    poststamp(11537,52002741,ID)
                    hatsuwa_flag = True
                    template_response(ID)

                elif(data == "talkmode off"):
                    post2one("対話モード終了",ID)
                    poststamp(11537,52002771,ID)
                    hatsuwa_flag = False
        
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

import cek
import logging


clova = cek.Clova(
    application_id="my.application.id", default_language="en", debug_mode=True)
    
NAME_flag = True

@app.route('/clova', methods=['POST'])
def my_service():
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response

@clova.handle.launch
def launch_request_handler(clova_request):
    global NAME_flag

    NAME_flag = True

    welcome = cek.Message(message=CLOVA_RES['WELCOME'], language="ja")
    response = clova.response([welcome])
    return response

@clova.handle.intent("name_intent")
def name(clova_request):
    global NAME_flag

    name = clova_request.slot_value('name_slot')

    if not(NAME_flag):
        print(CLOVA_RES['NAME2'])
        name2 = cek.Message(CLOVA_RES['NAME2'], language="ja")
        response = clova.response([name2])
        return response
    
    elif not(name):
        name_error = cek.Message(CLOVA_RES['NAME_ERROR'], language="ja")
        response = clova.response([name_error])
        return response
    
    else:
        print(name)
        NAME_flag = False
        notification(name)
        get_name = cek.Message(message = name + CLOVA_RES['GET_NAME'], language="ja")
        on_hold = cek.URL(ENDPOINT['RASPI2'] + "/resources/on_hold.mp3")
        default = cek.URL(ENDPOINT['RASPI2'] + "/resources/default.mp3")
        response = clova.response([get_name, on_hold, default])
        return response

@clova.handle.intent("show_intent")
def show(clova_request):
    global NAME_flag
    if NAME_flag:
        ask_name = cek.Message(CLOVA_RES['ASK_NAME'] , language="ja")
        response = clova.response([ask_name])
        return response
        
    else:
        try:
            print('かざした')
            res = snap_shot()
            res.json()
            data = res.json()
            print('写真のデータ',data['result'])
            #image_path = ENDPOINT['RASPI2'] + '/images/' + data['result']
            image_path = ENDPOINT['RASPI2'] + '/images/' + 'yarakasi.png'
            qr2url(image_path)
            template_response()
            show = cek.Message(message = CLOVA_RES['SHOW'], language="ja")
            on_hold = cek.URL(ENDPOINT['RASPI2'] + "/resources/on_hold.mp3")
            default = cek.URL(ENDPOINT['RASPI2'] + "/resources/default.mp3")
            response = clova.response([show, on_hold, on_hold, default])
            return response
        except:
            show_again = cek.Message(message = CLOVA_RES['SHOW_AGAIN'], language="ja")
            response = clova.response([show_again])
            return response

@clova.handle.intent("complete_intent")
def complete(clova_request):
    global NAME_flag

    if NAME_flag:
        ask_name = cek.Message(CLOVA_RES['ASK_NAME'] , language="ja")
        response = clova.response([ask_name])
        return response
        response = clova.response([plese_show])
    else:
        complete_res()
        complete = cek.Message(message = CLOVA_RES['COMPLETE'], language="ja")
        on_hold = cek.URL(ENDPOINT['RASPI2'] + "/resources/on_hold.mp3")
        default = cek.URL(ENDPOINT['RASPI2'] + "/resources/default.mp3")
        response = clova.response([complete, on_hold, default])
        return response

@clova.handle.intent("re_delivery_intent")
def re_delivery(clova_request):
    global NAME_flag
    if NAME_flag:
        ask_name = cek.Message(CLOVA_RES['ASK_NAME'] , language="ja")
        response = clova.response([ask_name])
        return response
    else:
        day = clova_request.slot_value('day_slot')
        post2admin(' パパがお忙しそうだったので伝言をうけトリました！')
        post2admin(day + '、再配達に来るそうです')
        poststamp('11537','52002736')
        tell = cek.Message(message = day + CLOVA_RES['TELL'], language="ja")
        response = clova.response([tell])
        return response

@clova.handle.default
def default_handler(request):
    global NAME_flag
    if NAME_flag:
        ask_name = cek.Message(CLOVA_RES['ASK_NAME'] , language="ja")
        response = clova.response([ask_name])
        return response
    else:
        post2admin('想定される返答が帰って来ませんでした、もう一度お願いします')
        template_response()
        default_message = cek.Message(message = CLOVA_RES['DEFAULT'], language="ja")
        on_hold = cek.URL(ENDPOINT['RASPI2'] + "/resources/on_hold.mp3")
        default = cek.URL(ENDPOINT['RASPI2'] + "/resources/default.mp3")
        response = clova.response([default_message, on_hold, default])
        return response

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
