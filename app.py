from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://pyo:jk1jk2jk3@cluster0.nygwmem.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



