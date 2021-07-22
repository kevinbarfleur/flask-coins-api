# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

API_URL = 'https://static.coinpaper.io/api/coins.json'


@app.route("/")
def getCoins():
    response = requests.get(API_URL)
    content = json.loads(response.content.decode('utf-8'))
    path = request.base_url

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'Error code: {}'.format(content['message'])
        }), 500

    data = []
    for coin in content:
        url = path + 'coin?id=' + coin['id']
        data.append(
            {
                "id": coin['id'],
                "link": url
            }
        )

    return jsonify({
        'status': 'ok',
        'data': data
    })


@app.route('/coin/')
def getCoin():
    coin = request.args.get('id')
    URL = 'https://static.coinpaper.io/api/coins/{}.json'.format(coin)

    response = requests.get(URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'Error code: {}'.format(content['message'])
        }), 500

    return jsonify({
        'status': 'ok',
        'data': content
    })


if __name__ == "__main__":
    app.run(debug=True)
