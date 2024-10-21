from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, add_entity

# Configure application
app = Flask(__name__)

# # Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///ltt.db")

# @app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():

    #Redirect logged in user
    if session.get("user_id"):
        flash("Please logout first!")
        return redirect("/")

    # via POST
    if request.method == "POST":

        # Clear session data
        session.clear()

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username is required!")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password is required!")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Username and/or password is invalid!")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(f"Logged in as {rows[0]['username']}!")
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out successfully!")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Look for invalid inputs
        if not request.form.get("username"):
            flash("Username is required!")
            return redirect("/register")
        elif not request.form.get('password'):
            flash("Password is required!")
            return redirect("/register")
        elif not request.form.get('confirmation'):
            flash("Password confirmation is required!")
            return redirect("/register")
        elif request.form.get('password') != request.form.get('confirmation'):
            flash("Password & password confirmation must be identical!")
            return redirect("/register")
        # Look for duplicate username
        if db.execute("SELECT * FROM users WHERE username = ?", request.form.get('username')):
            flash("Username already exists. Please select a different username!")
            return redirect("/register")
        # Password hashing and adding user to database
        pw = generate_password_hash(request.form.get('password'))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get('username'), pw)
        # Logging the user
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        flash(f"Logged in as {rows[0]['username']}!")
        return redirect("/")
    else:
        return render_template('register.html')

@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        return "TODO"
    else:
        return render_template("add_project.html")

@app.route("/add_lsp", methods=["GET", "POST"])
@login_required
def add_lsp():
    if request.method == "POST":
        return add_entity("lspname", "lsps", "lsp_name", "/add_lsp", db)
    else:
        return render_template("add_lsp.html")

@app.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    if request.method == "POST":
        return add_entity("accountname", "accounts", "account_name", "/add_account", db)
    else:
        return render_template("add_account.html")


# Debug mode
if __name__ == "__main__":
    app.run(debug=True)
