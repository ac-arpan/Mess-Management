# This should be the main backend file.
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import os
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    