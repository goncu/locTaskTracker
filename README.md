# Localization Task Tracker

## Introduction

Localization Task Tracker is a Flask app for freelance localization professionals to track their tasks. Users can add Language Service Providers (LSPs) they work with and accounts they work on, and create, edit, complete and delete projects.

## Features

### User Authentication

**Login**: Users can log in with a username and password. Passwords are securely hashed using werkzeug.security's generate_password_hash.

![Alt text](assets/login.png)

**Registration**: New users can register for an account by providing a username and password. There is basic server-side validation.

![Alt text](assets/register.png)

**Logout**: Users can securely log out of the application.

### Project Managament

**Add Project**: Users can add new projects by specifying details such as LSP, account, task type (e.g., editing, translation), date, time, and word count. The app automatically calculates weighted words based on the task type.

![Alt text](assets/add_project.png)

**Edit Project**: Users can modify the details of existing projects.

![Alt text](assets/edit_project.png)

**Delete Project**: Users can delete projects they no longer wish to track for any reason.

![Alt text](assets/delete_project.png)

**Mark as Complete**: Projects can be marked as completed, which will remove them from the active project list.

![Alt text](assets/complete_project.png)

### Sorting

**Sort Projects**: Projects can be sorted based on different criteria such as project name or weighted word count, to provide an organized view of ongoing tasks.

![Alt text](assets/index.png)

### Data Validation & Error Handling

**Input Validation**: Input validation ensures that no invalid data (e.g., negative word counts or missing fields) is entered.

![Alt text](assets/validation.png)

**Flash Messages**: The app provides real-time feedback using flash messages for actions like logging in, adding projects, or encountering errors.

![Alt text](assets/flash.png)

### Database Structure

This application uses an SQLite database (ltt.db) with the following tables:

**Users**: This table stores unique user IDs, usernames and hashed passwords.

**Projects**: This table stores project data, such as word count, due date, project name, etc.

**LSPs**: This table stores LSPs added by the user. Added items are linked with user, meaning only they can access them.

**Accounts**: This table stores accounts added by the user. Added items are linked with user, meaning only they can access them.

## Running the App

**1.** Clone the repository:

```
git clone https://github.com/goncu/locTaskTracker.git
cd locTaskTracker
```

**2.** Create a virtual environment:

```
python3 -m venv venv
```

**3.** Activate the virtual environment:

- On macOS/Linux:

```
source venv/bin/activate
```

- On Windows:

```
venv\Scripts\activate
```

**4.** Install required dependencies:

```
pip install -r requirements.txt
```
