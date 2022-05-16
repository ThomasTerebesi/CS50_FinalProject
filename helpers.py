from functools import wraps
from flask import flash, redirect, request, session
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

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, note TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));");
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, description TEXT NOT NULL, status INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(id));")
    cur.execute("CREATE TABLE IF NOT EXISTS timers (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, seconds INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(id));")

    con.commit()
    con.close()

def move_task(id, n = 0):
    """
    Change a task's status by n.
    """

    # If n is not set, there is no need to execute all the code
    if n == 0:
        flash("# move_task(): n was not set")
        return redirect("/tasks")

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    

    if id:
        cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", [id, session["user_id"]])
        task = cur.fetchone()
        print(task)
        if not task:
            flash("task does not exist for this user")
            return redirect("/tasks")
        # Task may not have a status smaller than zero
        elif task[3] + n < 0:
            cur.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", [0, id, session["user_id"]])
            con.commit()
        # Task may not have a status larger than two
        elif task[3] + n > 2:
            cur.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", [2, id, session["user_id"]])
            con.commit()
        else:
            # Modify the status value contained in task[3] by n
            cur.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", [task[3] + n, id, session["user_id"]])
            con.commit()
    
    con.close()


