from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import ensure_database, login_required, move_task
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3


# Configure Flask
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure that there is a database with the correct tables
ensure_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register the user.
    """

    if request.method == "POST":
        # Configure SQLite3
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Ensure username has been submitted
        if not escape(request.form.get("username")):
            flash("must provide username")
            con.close()
            return render_template("register.html")
        
        # Check if username already exists in database
        cur.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        if cur.fetchone() == escape(request.form.get("username")):
            flash("username already exists")
            con.close()
            return render_template("register.html")

        # Ensure that email address has been submitted
        if not escape(request.form.get("email")):
            flash("must provide email address")
            con.close()
            return render_template("register.html")

        # Check if email address already exists in database
        cur.execute("SELECT * FROM users WHERE email = ?", [escape(request.form.get("email"))])
        if cur.fetchone() == escape(request.form.get("email")):
            flash("email address already in use")
            con.close()
            return render_template("register.html")

        # Check if password has been submitted
        if not escape(request.form.get("password")):
            flash("must provide a password")
            con.close()
            return render_template("register.html")

        # Check if password confirmation has been submitted
        if not escape(request.form.get("password")):
            flash("must provide password confirmation")
            con.close()
            return render_template("register.html")

        # Ensure that password and password confirmation match
        if not escape(request.form.get("password")) == escape(request.form.get("confirmation")):
            flash("passwords do not match")
            con.close()
            return render_template("register.html")

        # Create new user in database
        cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", [escape(request.form.get("username")), escape(request.form.get("email")), generate_password_hash(escape(request.form.get("password")))])
        con.commit()
        con.close()
    
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log the user in.
    """
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Configure SQLite3
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Ensure username has been submitted
        if not escape(request.form.get("username")):
            flash("must provide username")
            con.close()
            return render_template("login.html")

        # Ensure password has been submitted
        if not escape(request.form.get("password")):
            flash("must provide password")
            con.close()
            return render_template("login.html")

        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = ?", [escape(request.form.get("username"))])
        user = cur.fetchall()

        if not user:
            flash("invalid username")
            con.close()
            return render_template("login.html")

        if not check_password_hash(user[0][3], escape(request.form.get("password"))):
            flash("invalid password")
            con.close()
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = user[0][0]

        con.close()
        
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log the user out.
    """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """
    Manage task creation.
    """

    # Configure SQLite3
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    if request.method == "POST":
        # Check if a new item has been provided
        if not escape(request.form.get("newtask")):
            flash("empty task will not be saved")
            con.close()
            return redirect("/tasks")

        # Check if status value is correct
        status = request.form.get("status")
        if not (status == "todo" or status == "inprogress" or status == "done"):
            flash("invalid status")
            con.close()
            return redirect("/tasks")

        # Generate status code
        status_code = 0
        if status == "todo":
            status_code = 0
        elif status == "inprogress":
            status_code = 1
        elif status == "done":
            status_code = 2
        else:
            flash("invalid status")
            con.close()
            return redirect("/tasks")     
        
        # Add task to database
        cur.execute("INSERT INTO tasks (user_id, description, status) VALUES (?, ?, ?)", [session["user_id"], escape(request.form.get("newtask")), status_code])
        con.commit()
        con.close()

        return redirect("/tasks")

    else:
        # Get tasks from DB
        cur.execute("SELECT id, description, status FROM tasks WHERE user_id = ?", [session["user_id"]])
        tasks = cur.fetchall()
        con.close()

        # print(tasks)

        # TODO: If possible, replace '\n' characters

        return render_template("tasks.html", tasks=tasks)


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    """
    Manage note creation.
    """
    # Configure SQLite3
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    if request.method == "POST":
        # Check if a new note has been provided
        if not escape(request.form.get("newnote")):
            flash("empty note will not be saved")
            con.close()
            return redirect("/notes")
        
        # Add note to database
        cur.execute("INSERT INTO notes (user_id, note) VALUES (?, ?)", [session["user_id"], escape(request.form.get("newnote"))])
        con.commit()
        con.close()

        return redirect("/notes")

    else:
        # Get notes from DB
        cur.execute("SELECT id, note FROM notes WHERE user_id = ?", [session["user_id"]])
        notes = cur.fetchall()
        con.close()

        # TODO: If possible, replace '\n' characters

        return render_template("notes.html", notes=notes)


@app.route("/removenote", methods=["GET", "POST"])
@login_required
def remove_note():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        id = request.form.get("id")
        if id:
            cur.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", [id, session["user_id"]])
            con.commit()
        
        con.close()

        return redirect("/notes")

    else:
        flash("cannot remove a note like this")
        return redirect("/notes")


@app.route("/editnote", methods=["GET", "POST"])
@login_required
def edit_note():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        note = ""
        id = request.form.get("id")
        if id:
            cur.execute("SELECT id, note FROM notes WHERE id = ? AND user_id = ?", [id, session["user_id"]])
            note = cur.fetchone()

        return render_template("editnote.html", id = note[0], note = note[1])
        
    else:
        flash("cannot edit a note like this")
        return redirect("/notes")


@app.route("/submitnoteedit", methods=["GET", "POST"])
@login_required
def submit_note_edit():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        id = request.form.get("id")
        edited_note = escape(request.form.get("editednote"))

        if id:
            cur.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", [id, session["user_id"]])
            note = cur.fetchone()
            if not note:
                flash("note does not exist for this user")
                return redirect("/notes")
            else:
                cur.execute("UPDATE notes SET note = ? WHERE id = ? AND user_id = ?", [edited_note, id, session["user_id"]])
                con.commit()
        
        con.close()

        flash("Note edit success!")
        return redirect("/notes")
        
    else:
        flash("cannot submit an edited note like this")
        return redirect("/notes")


@app.route("/removetask", methods=["GET", "POST"])
@login_required
def remove_task():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        id = request.form.get("id")
        if id:
            cur.execute("DELETE FROM tasks WHERE id = ?  AND user_id = ?", [id, session["user_id"]])
            con.commit()
        
        con.close()

        return redirect("/tasks")

    else:
        flash("cannot remove a task like this")
        return redirect("/tasks")


@app.route("/edittask", methods=["GET", "POST"])
@login_required
def edit_task():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        task = ""
        id = request.form.get("id")
        if id:
            cur.execute("SELECT id, description, status FROM tasks WHERE id = ? AND user_id = ?", [id, session["user_id"]])
            task = cur.fetchone()

        return render_template("edittask.html", id = task[0], description = task[1], status = task[2])
        
    else:
        flash("cannot edit a task like this")
        return redirect("/tasks")


@app.route("/submittaskedit", methods=["GET", "POST"])
@login_required
def submit_task_edit():
    if request.method == "POST":
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        id = request.form.get("id")
        edited_description = escape(request.form.get("editedtask"))
        edited_status = request.form.get("status")

        # Generate status code
        status_code = 0
        if edited_status == "todo":
            status_code = 0
        elif edited_status == "inprogress":
            status_code = 1
        elif edited_status == "done":
            status_code = 2
        else:
            flash("invalid status")
            con.close()
            return redirect("/tasks")  

        if id:
            cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", [id, session["user_id"]])
            note = cur.fetchone()
            if not note:
                flash("task does not exist for this user")
                return redirect("/notes")
            else:
                cur.execute("UPDATE tasks SET description = ?, status = ? WHERE id = ? AND user_id = ?", [edited_description, status_code, id, session["user_id"]])
                con.commit()
        
        con.close()

        flash("Task edit success!")
        return redirect("/tasks")
        
    else:
        flash("cannot submit an edited task like this")
        return redirect("/tasks")


@app.route("/nextstatus", methods=["GET", "POST"])
@login_required
def next_status():
    if request.method == "POST":
        # Go to next status, increasing it by 1
        move_task(request.form.get("id"), 1)
        return redirect("/tasks")

    else:
        flash("cannot move a task like this")
        return redirect("/tasks")


@app.route("/prevstatus", methods=["GET", "POST"])
@login_required
def previous_status():
    if request.method == "POST":
        # Go to previous status, decreasing it by 1
        move_task(request.form.get("id"), -1)
        return redirect("/tasks")

    else:
        flash("cannot move a task like this")
        return redirect("/tasks")


@app.route("/timer")
@login_required
def timer():
    # TODO
    return render_template("timer.html")


@app.route("/addtimer")
@login_required
def add_timer():
    return()