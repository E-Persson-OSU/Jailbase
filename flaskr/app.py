from flask import Flask, render_template

import services.jailbase as jb
import services.db as db
import os
import threading
import http.client as client
import time


"""global variables"""
conn = client.HTTPSConnection("http://127.0.0.1/", 5000)

app = Flask(__name__)

"""@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("Run recurring task")
            time.sleep(3)

    thread = threading.Thread(target=run_job)
    thread.start()"""

"""def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = conn.request("GET", "/")
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()"""

if __name__ == "__main__":
    app.run()

def init_db():
    db = db.get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    db.init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    records = jb.getrecent()
    return render_template('jailbase.html', records=records)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')