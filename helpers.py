from functools import wraps
from flask import flash, redirect, session
from io import BytesIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import base64

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


def generate_task_stats():
    """
    Generates statistics for existing tasks.
    """

    labels = []
    sizes = []

    # Call separate function to add data to the two lists above
    check_and_append(labels, sizes)

    # Do not generate statistics if there is no data
    if len(labels) == 0:
        return None
    
    # Generate plot
    plt.style.use('seaborn-pastel')

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=None, labels=labels, autopct="%1.1f%%", shadow=False, startangle=90)
    ax.axis("equal")
    fig.set_facecolor("#f3f3f3")

    # Save plot as image URL
    img = BytesIO()
    plt.savefig(img, format="png", bbox_inches='tight')
    plt.close()
    img.seek(0)
    img_url = base64.b64encode(img.getvalue()).decode("utf8")

    return(img_url)


def check_and_append(labels = [], sizes = []):
    """
    Checks whether tasks exist and appends their data to the supplied lists, depending on the tasks respective status.
    """

    label = ""

    # Loop through each status
    for status in range(3):
        if status == 0:
            label = "To Do"
        elif status == 1:
            label = "In Progress"
        elif status == 2: 
            label = "Done"

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("SELECT * FROM tasks WHERE status = ? AND user_id = ?", [status, session["user_id"]])
        tasks = cur.fetchall()

        # If there are any tasks for this status...
        if len(tasks) > 0:
            # ... append the respective status label ...
            labels.append(label)
            # ... and number of tasks with that status
            sizes.append(len(tasks))

        con.close()