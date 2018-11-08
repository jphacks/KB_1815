import uuid
import shelve
import os
import re
import json
# from pyzbar.pyzbar import decode
# import fastzbarlight
import io
import urllib.request
from flask import (
    Flask, request, session, abort, render_template, redirect
)
import requests
from flask_bootstrap import Bootstrap
from PIL import Image
import time

app = Flask(__name__, static_folder='static')
app.secret_key = 'weqc4930252xarqkslgj3c4c1m1rj2ej'
bootstrap = Bootstrap(app)


class LinePay(object):

    DEFAULT_ENDPOINT = 'sandbox-api-pay.line.me/'
    VERSION = 'v2'

    def __init__(self, channel_id, channel_secret, redirect_url):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.redirect_url = redirect_url

    def reserve(self, product_name, amount, currency, order_id, **kwargs):
        session['secret'] = channel_secret
        session['resave'] = False
        session['saveUninitialized'] = False
        self.DEFAULT_ENDPOINT = request.environ['HTTP_HOST']
        if self.DEFAULT_ENDPOINT[-1] != '/':
            self.DEFAULT_ENDPOINT += '/'
        print(self.DEFAULT_ENDPOINT)
        url = 'https://{}{}{}'.format(self.DEFAULT_ENDPOINT, self.VERSION, '/payments/request')

        print('url', url)
        data = {**
                {
                    'productName': product_name,
                    'amount': amount,
                    'currency': currency,
                    # 'confirmUrl': 'https://3dwke93g5m.execute-api.ap-northeast-1.amazonaws.com/dev/pay/confirm',
                    'confirmUrl': 'https://{}{}'.format(request.environ['HTTP_HOST'], self.redirect_url),
                    # 'confirmUrl': 'https://ghjm2z26h7.execute-api.ap-northeast-1.amazonaws.com/LinaPay_uketori' + self.redirect_url,
                    'orderId': order_id,
                },
                **kwargs}
        headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.channel_id,
            'X-LINE-ChannelSecret': self.channel_secret
        }
        print('headers', headers)
        print('data', json.dumps(data).encode("utf-8"))
        response = requests.post(url, headers=headers, data=json.dumps(data).encode("utf-8"))
        print('response', response.text)
        if int(json.loads(response.text)['returnCode']) == 0:
            with shelve.open('store') as store:
                # just for prototyping
                store[str(json.loads(response.text)['info']['transactionId'])] = {
                    'productName': product_name, 'amount': amount, 'currency': currency}
            return json.loads(response.text)

        else:
            abort(400, json.loads(response.text)['returnCode'] + ' : ' + json.loads(response.text)['returnMessage'])

    def confirm(self, transaction_id):
        transaction_info = {}
        with shelve.open('store') as store:
            transaction_info = store[transaction_id]

        if len(transaction_info) == 0:
            abort(400, 'reservation of this transaction id is not exists')

        url = 'https://{}{}{}'.format(self.DEFAULT_ENDPOINT, self.VERSION, '/{}/confirm'.format(transaction_id))
        data = {
            'amount': transaction_info['amount'],
            'currency': transaction_info['currency'],
        }
        headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.channel_id,
            'X-LINE-ChannelSecret': self.channel_secret
        }
        response = requests.post(url, headers=headers, data=json.dumps(data).encode("utf-8"))
        return transaction_info

# get it in https://pay.line.me/jp/developers/techsupport/sandbox/creation?locale=ja_JP


# chennel_id = os.environ['LINE_PAY_CHANNEL_ID']
# channel_secret = os.environ['LINE_PAY_CHANNEL_SECRET']
# chennel_id = '1616116834'
# channel_secret = '8350bc210dfdeb04b9d1488a683b98cc'
chennel_id = '1620433176000'
channel_secret = 'b0a87caa5aeb04aa04cc4cb0c08e8af9'
callback_url = '/confirm'

pay = LinePay(chennel_id, channel_secret, callback_url)

@app.route("/")
def render_index():
    return render_template('index.html')

@app.route("/test")
def render_test():
    return render_template('test.html')

@app.route("/reserve")
def redirect_to_pay():
    data = {
        "product_name": "LINE Pay Demo product",
        'amount': '100',
        'currency': 'JPY',
        'order_id': uuid.uuid4().hex,
        # optional values can be set. see https://pay.line.me/file/guidebook/technicallinking/LINE_Pay_Integration_Guide_for_Merchant-v1.1.2-JP.pdf
        'productImageUrl': 'https://{}{}'.format(request.environ['HTTP_HOST'], '/static/item_image.png')
    }
    transaction_info = pay.reserve(**data)
    return redirect(transaction_info['info']['paymentUrl']['web'])

@app.route("/callback")
def callback_from_pay():
    transaction_info = pay.confirm(request.args.get('transactionId'))
    return render_template('purchased.html', **transaction_info)


app.errorhandler(400)
def handler_error_400(error):
    return error

# @app.route('/qr2url', methods=['POST'])
# def qr2url():
#     time.sleep(3)
#     data = request.data.decode('utf-8')
#     data = json.loads(data)
#     url = data['image_path']
#     f = io.BytesIO(urllib.request.urlopen(url).read())
#     img = decode(Image.open(f))
#     url = img[0][0].decode('utf-8', 'ignore')
#     return json.dumps({'url': url})


if __name__ == '__main__':
    print('Hello main function')
    app.debug = True
    app.run(host='0.0.0.0')
