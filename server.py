from flask import Flask, request, abort
import json , config
from binance.client import Client
from binance.enums import *


app = Flask(__name__)

def linenotify_message(TOKEN1,message):
  url = 'https://notify-api.line.me/api/notify'
  ###LINE Notify Token###
  data = {'message': message}
  headers = {'Authorization':'Bearer ' + TOKEN1}
  session = requests.Session()
  session_post = session.post(url, headers=headers, data = data)
  #session_post = session.post(url, headers=headers,data =data)
  print(session_post.text)
    
@app.route('/webhook_3', methods=['POST'])
def webhook_3():
    if request.method == 'POST':
        data = json.loads(request.data)
        client = Client(data["API_KEY"],data["API_SECRET"])
        print("Symbol: "+data["symbol"]+"Status: "+data["cmd"]+"Amount: "+data["amount"])
        if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
            return {"code":"error", "message":"Nice try, incalid passphrase"}
        elif data['cmd'] == 'long' or data['cmd'] == 'Long' or data['cmd'] == 'LONG':
            order_long = client.futures_create_order(symbol=data['symbol'], side='BUY',positionSide='LONG', type='MARKET', quantity=data['amount'])
            #linenotify_message(TOKEN1,message)
            return order_long
        elif data['cmd'] == 'short' or data['cmd'] == 'Short' or data['cmd'] == 'SHORT':
            order_short = client.futures_create_order(symbol=data['symbol'], side='SELL',positionSide='SHORT', type='MARKET', quantity=data['amount'])
            return order_short
        elif data['cmd'] == 'close_long':
            close_long = client.futures_create_order(symbol=data['symbol'], side='SELL',positionSide='LONG', type='MARKET', quantity=data['amount'])
            return close_long
        elif data['cmd'] == 'close_short':
            close_short = client.futures_create_order(symbol=data['symbol'], side='BUY',positionSide='SHORT', type='MARKET', quantity=data['amount'])
            return close_short
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=False)
