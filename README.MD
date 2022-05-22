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
`/tasks` checks ensures that a newly created task is valid. It is also used to render the contents of `tasks.html` after each of the other task-related routes. When rendering the page, `generate_task_stats()` from `helpers.py` is called to generate the task statistics seen at the bottom of the task list.

The following routes execute one task and then redirect back to `/tasks`:

`/removetask` handles task removal.

`/edittask` handles task editing.

`/submitedittask` handles the submission of an edited task.

`/nextstatus` and `/prevstatus` move a task to the next or previous status, respectively. To achieve that, they use the `move_task()` helper function defined in `helpers.py`.

### Notes


### Timer

### `helpers.py`

## Future Improvements




