# Prodozo
#### Video Demo:  https://youtu.be/F2e5_FgT-ts
#### Description: 
Prodozo is a web application that allows the user to use three productivity tools: A task tracker, a note-taking tool and a timer.

## Usage
Download the files in this repository and use the `flask run` command in the root folder.

## Structure
The structure of the app is mostly defined in `app.py` through the Flask backend. Helper functions can be found in `helpers.py`. The main routes in `app.py` can roughly be split into the following areas:

### Account Management
`/register` allows the user to register themselves. Checks are performed to ensure that the account to be created does contain valid information or that the new data does not conflict with the data in existing accounts. Passwords are saved with `generate_password_hash()`, so that they cannot be accessed in cleartext form.

`/login` allows the user to log in and access the data of an already existing account. Once the user is logged in, their unique ID will be stored in the session. Once an ID can be read, the menu items will be displayed (see `layout.html`). The user's ID will be used in all database-related actions to make sure that the data the currently logged in user receives belongs to them and only them.

`/logout` logs out the user. It clears the active session, which means that the user's ID is forgotten, and redirects them to `/`.

### Tasks
`/tasks` ensures that a newly created task is valid. It is also used to render the contents of `tasks.html` after each of the other task-related routes. When rendering the page, `generate_task_stats()` from `helpers.py` is called to generate the task statistics seen at the bottom of the task list.

The following routes execute one task and then redirect back to `/tasks`:

`/removetask` handles task removal.

`/edittask` handles task editing.

`/submittaskedit` updates the edited task.

`/nextstatus` and `/prevstatus` move a task to the next or previous status, respectively. To achieve that, they use the `move_task()` helper function defined in `helpers.py`.

### Notes
`/notes` renders the contents of `notes.html`. It also makes sure that new notes are valid. 

The routes below redirect to `/notes`:
`/removenote` handles note removal.

`/editnote` handles note editing.

`/submitnoteedit` updates the edited note.

### Timer
`timer` redirects to `timer.html`; this page embeds `timer.js`, which contains the logic for how the timer tool works. This is also the only JavaScript used on this project. The timer was created with fairly basic JavaScript functionality, the interesting parts are how the presets are handled and how setting, resetting and clearing intervals is managed in basically all functions.

### `helpers.py`
A couple of the functions contained in `helpers.py` have already been mentioned above. It also contains:

* A decorator function called `login_required()` that ensures that most routes can only be accessed with while in a session with an active user ID.

* An `ensure_database()` function that makes sure that there is a database file with the right schema, or, if there is not, that it is created.

## Potential Improvements
There's some functionality that was initially planned for but was dropped in order to not suffer from feature creep and never finish the project:
* Implementing proper handling of newline characters in user input.
* Task tracker functionality:
    * Prevent reloading the page after changing the status of or removing a task
    * Editing without redirecting to another page
    * Keep track of
        * Task's creation date
        * Deadline(s) set by the user
* Timer functionality:
    * Flashier effects when the timer finishes
    * Store some of the values used by the user so they can re-use them later




