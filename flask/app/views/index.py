from flask import redirect, url_for, render_template, request, session

from app import app, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.pug')
