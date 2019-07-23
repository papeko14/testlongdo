from flask import Flask, request, abort
import requests
import json
from test import *
from uncleengineer import thaistock



app = Flask(__name__)
Channel_access_token = "ENcqjwF/NJjmLRxvEguzkDDT8YpTX2w85jwPzlFhwRh7/qflNYnH7vVkyggqDVwQUJg7QD+VD2YRkJ56d3RSCex/CeHAmqLAybjGAD/bnXgJ0Ci+ijkVE9LfQBQm+2AI7FZE8PsuRCE5cdynYzIVhwdB04t89/1O/w1cDnyilFU="

def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE




@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'bii' in message :
            ITD = thaistock('ITD')
            Reply_messasge = ('อ้วนมาก ')
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif "btc" in message :
            Reply_messasge = 'ราคา BITCOIN ขณะนี้ : {}'.format(GET_BTC_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)


        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world book',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200