from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://pyo:jk1jk2jk3@cluster0.nygwmem.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/main', methods=['POST'])
def upload_music():
    url_receive = request.form['url_give']
    genre_receive = request.form['genre_give']
    print(url_receive,genre_receive)
    doc = {
        'url': url_receive,
        'genre': genre_receive
    }
    # db.테이블.insert_one(doc)
    return jsonify({'msg': '등록완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



