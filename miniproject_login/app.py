from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'secret'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.gfgemqc.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
def home_login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.minilogin.find_one({"username": payload["id"]})
        return render_template('home.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("home", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("home", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/select')
def select():
    return render_template('select.html')


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.minilogin.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.minilogin.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": nickname_receive,  # 프로필 이름 기본값은 닉네임
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.minilogin.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.minilogin.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        nickname_receive = request.form["nickname_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": nickname_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.minilogin.update_one({'username': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def music_posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.minilogin.find_one({"username": payload["id"]})
        url_receive = request.form['url_give']
        result = db.minisong.find_one({"melon_url": url_receive})
        if result is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            data = requests.get(url_receive, headers=headers)

            soup = BeautifulSoup(data.text, 'html.parser')

            div = soup.select_one('#downloadfrm > div > div > div.entry')
            title = div.select_one('div.info > div.song_name').get_text(strip=True).lstrip("곡명")
            artist = div.select_one('div.artist').text
            # downloadfrm > div > div > div.entry > div.info > div.artist
            album_title = div.select_one('div.meta > dl > dd:nth-child(2) > a').get_text()
            album_img = soup.select_one('#downloadfrm > div > div > div.thumb > a > img')["src"]
            genre = div.select_one('div.meta > dl > dd:nth-child(6)').get_text()

            print(title, artist, album_title, album_img, genre)

            doc = {
                "username": user_info["username"],
                "profile_name": user_info["profile_name"],
                "profile_pic_real": user_info["profile_pic_real"],
                'melon_url': url_receive,
                'title': title,
                'artist': artist,
                'album_title': album_title,
                'album_img': album_img,
                'genre': genre
            }
            db.minisong.insert_one(doc)
            return jsonify({"result": "success", 'msg': '포스팅 성공'})
        else:
            return jsonify({'msg': '이미 등록된 URL입니다!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/posting", methods=['GET'])
def get_posts():
    username_receive = request.args.get("username_give")
    if username_receive == "":
        posts = list(db.minisong.find({}, {'_id': False}))
    else:
        posts = list(db.minisong.find({"username": username_receive}, {'_id': False}))
    return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.minilogin.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "username": user_info["username"],
            "type": type_receive
        }
        if action_receive == "like":
            db.minilikes.insert_one(doc)
        else:
            db.minilikes.delete_one(doc)
        count = db.minilikes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
