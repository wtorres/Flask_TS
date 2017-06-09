from app import app, db, models
from flask import request, render_template

@app.route('/')
@app.route('/index')

def index():
    return "Hello, View Home!"
    #user =  {'nickname': 'Axel Mauricio'}

