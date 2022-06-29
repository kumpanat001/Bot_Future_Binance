from flask import Flask, request, abort
import json , config
from binance.client import Client
from binance.enums import *

app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = json.loads(request.data)
        client = Client(data["API_KEY"],data["API_SECRET"])
        print("Symbol"+ data["symbol"]+data["cmd"]+data["amount"])
        if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
            print(data['passphrase'])
            return {"code":"error", "message":"Nice try, incalid passphrase"}
        if data['cmd'] == 'buy' or data['cmd'] == 'Buy' or data['cmd'] == 'BUY':
            order_buy = client.futures_create_order(symbol=data['symbol'], side='BUY', type='MARKET', quantity=data['amount'])
            return order_buy
        if data['cmd'] == 'sell' or data['cmd'] == 'Sell' or data['cmd'] == 'SELL':
            order_sell = client.futures_create_order(symbol=data['symbol'], side='SELL', type='MARKET', quantity=data['amount'])
            return order_sell
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=False)