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
    result = db.main.find_one({"melon_url":url_receive})
    if result == None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        div = soup.select_one('#downloadfrm > div > div > div.entry')
        title = div.select_one('div.info > div.song_name').get_text(strip= True).lstrip("곡명")
        artist = div.select_one('div.artist').text
        # downloadfrm > div > div > div.entry > div.info > div.artist
        album_title = div.select_one('div.meta > dl > dd:nth-child(2) > a').get_text()
        album_img = soup.select_one('#downloadfrm > div > div > div.thumb > a > img')["src"]
        genre = div.select_one('div.meta > dl > dd:nth-child(6)').get_text()

        print(title,artist,album_title,album_img,genre)

        doc = {
            'melon_url': url_receive,
            'title':title,
            'artist': artist,
            'album_title': album_title,
            'album_img':album_img,
            'genre':genre
        }
        db.main.insert_one(doc)
        return jsonify({'msg': '등록완료!'})
    else:
        return jsonify({'msg':'이미 등록된 URL입니다!'})

@app.route("/main", methods=["GET"])
def music_get():
    music_list = list(db.main.find({}, {'_id': False}))
    return jsonify({'musics':music_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


