from functools import wraps
from flask import redirect, session
from os.path import exists

import sqlite3

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def ensure_database():
    """
    Ensure that there is a database with the right schema.
    """

    print("yes")

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, note TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));");
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, description TEXT NOT NULL, status INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(id));")

    con.commit()
    con.close()


