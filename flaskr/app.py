from flask import Flask, render_template

import services.jailbase as jb
import services.db as db
import http.client as client
import time



"""global variables"""
app = Flask(__name__)

@app.before_first_request
def init():
    db.init_db(app.root_path)
    print("Initializing DB before first request...")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    records = jb.getrecent()
    db.updatesourceids(jb.getsourceids())
    return render_template('jailbase.html', records=records)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')