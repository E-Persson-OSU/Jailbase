import sqlite3

import click
from flask import current_app
import os

"""global variables"""
rel_dir = "\static\db\schema.sql"


def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row

    return db

""" def init_db():
    db = get_db()
    Instead of using a schema, just make one db and table
    cur = db.cursor()
    cur.execute('DROP TABLE if EXISTS recents')
    cur.execute('DROP TABLE if EXISTS sourceids')
    cur.execute('CREATE TABLE recents (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, bookdate TEXT, mugshot TEXT)')
    cur.execute('CREATE TABLE sourceids (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sourceid TEXT)')
    db.commit()
    db.close() """

def init_db(absolute_dir):
    db = get_db()
    abs_file_path = absolute_dir + rel_dir
    print(abs_file_path)
    with current_app.open_resource(abs_file_path) as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()
    db.close()



def addrecentdb(recents):
    db = get_db()
    cursor = db.cursor()
    for recent in recents:
        cursor.execute("INSERT INTO recents VALUES (?,?,?,?)", (None, recent['name'], recent['book_date'], recent['mugshot']))
    db.commit()

def getrecentdb():
    records = {
        "name":"",
        "book_date": "",
        "mugshot": ""
    }
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recents")
    rows = cursor.fetchall()
    for row in rows():
        records["name"] = row[1]
        records["book_date"] = row[2]
        records["mugshot"] = row[3]
    data = {"records": records}
    return data
    
def updatesourceids(sourceids):
    db = get_db()
    cursor = db.cursor()
    table_name = 'sourceids'

    for sourceid in sourceids:
        print(sourceid)
        """sqlite3 does not like dashes. need to remove dash from string to store, add dash back when I need to take the sourceids out again"""
        select_query = f"SELECT * FROM {table_name} WHERE sourceid = {sourceid}"
        cursor.execute(select_query)
        existing_row = cursor.fetchone()

        if existing_row is None:
            insert_query = f"INSERT INTO {table_name} (id, sourceid) VALUES (?, ?)"
            cursor.execute(insert_query, (None, sourceid))
            db.commit()
            print("New SourceID Added\n")
        else:
            print("SourceID already exists\n")
    db.close()

    

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')