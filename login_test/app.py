from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import jwt
import hashlib
from datetime import datetime, timedelta

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.gfgemqc.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/sign')
def register():
    return render_template('register.html')


@app.route('/api/login')
def login():
    return render_template('login.html')


# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/sign', methods=['GET', 'POST'])
def api_register():
    print(request.form)
    input_data = request.form
    id_receive = input_data['id_give']
    pw_receive = input_data['pw_give']
    pw2_receive = input_data['pw2_give']
    nickname_receive = input_data['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    pw2_hash = hashlib.sha256(pw2_receive.encode('utf-8')).hexdigest()
    print(pw_hash, pw2_hash)

    user = db.login_test.find_one({'id': id_receive})

    if user is not None:
        return jsonify({'result': 'fail', 'msg': '이미 가입된 ID입니다.!!'})

    else:
        if pw_hash == pw2_hash:
            doc = {
                'id': id_receive,
                'password': pw_hash,
                'password2': pw2_hash,
                'nickname': nickname_receive
            }
            db.login_test.insert_one(doc)
            return jsonify({'result': 'success', 'token': pw_hash, 'msg': '가입완료!!'})

        else:
            return jsonify({'result': 'fail', 'msg': '비밀번호가 일치하지 않습니다!!'})


SECRET_KEY = 'secret'


@app.route("/api/login", methods=["POST"])
def web_login_post():
    print(request.form)
    input_data = request.form
    id_receive = input_data['id_give']
    pw_receive = input_data['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print(pw_hash)

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    user = db.login_test.find_one({'id': id_receive, 'password': pw_hash})

    # 아이디, 비밀번호가 일치하는 경우
    if user is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=5)  # 로그인 24시간 유지
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 완료!'})

    # 아이디, 비밀번호가 일치하지 않는 경우
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 실패!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
