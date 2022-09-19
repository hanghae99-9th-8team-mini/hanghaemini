import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://pyo:jk1jk2jk3@cluster0.nygwmem.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}




@app.route('/')
def home():
    return render_template('index.html')

@app.route("/news", methods=["POST"])
def web_mars_post():
    for i in range(20):
        db.teamproject.delete_one({})
    data = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    content = soup.find('div', id='main_content')
    headline = content.find('div', '_persist')
    groups = headline.find_all(attrs={'class': 'cluster_group'})

    for group in groups:

        group_body = group.find('div', 'cluster_body')
        cluster_thumb = group_body.find('div', 'cluster_thumb')
        link = cluster_thumb.find('a').attrs['href']
        img = cluster_thumb.find('img').attrs['src']
        cluster_text = group_body.find('div', 'cluster_text')
        title = cluster_text.find('a').text
        p = cluster_text.find('div', 'cluster_text_lede').text
        doc = {'link':link,
               'img':img,
               'title':title,
               'p':p
        }
        db.teamproject.insert_one(doc)
    return jsonify({'msg': '불러오기 완료!'})

@app.route("/news", methods=["GET"])
def web_mars_get():
    news_list = list(db.teamproject.find({}, {'_id': False}))
    return jsonify({'newslist': news_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)






