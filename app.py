import os
from os.path import join, dirname
from dotenv import load_dotenv

from http import client
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_recive = request.args.get('sample_give')
    # print(sample_recive)
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary' , methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files["profile_give"]
    profilename = f'profile-{mytime}.{extension}'
    save_to = f'static/{profilename}'
    profile.save(save_to)

    timepost = today.strftime('%Y.%m.%d')


    doc = {
    'file': filename,
    'profile': profilename,
    'title': title_receive,
    'content': content_receive,
    'timepost': timepost
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Data Tersimpan'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)