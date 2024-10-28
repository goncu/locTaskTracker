from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import add_entity, login_required, sorting

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
    user_id = session["user_id"]
    projects = db.execute("SELECT * FROM projects WHERE user_id = ?  AND completed = ? ORDER BY date_time", user_id, 'no')
    return render_template("index.html", projects=projects)

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
    user_id = session["user_id"]
    today = datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        # Storing form data into variables
        lspname = request.form.get("lspname")
        accountname = request.form.get("accountname")
        projectname = request.form.get("projectname")
        date = request.form.get("date")
        time = request.form.get("time")
        date_time = f"{date} {time}"
        tasktype  = request.form.get("tasktype")     
        newwords = request.form.get("newwords")
        highfuzzy = request.form.get("highfuzzy")
        lowfuzzy = request.form.get("lowfuzzy")
        hundredpercent = request.form.get("hundredpercent")
        hourlywork = request.form.get("hourlywork")
        if tasktype == "editing":
            weighted_words = int(newwords) + int(highfuzzy) + int(lowfuzzy) + int(hundredpercent)
        else:
            weighted_words = round((int(newwords) if tasktype != "mtpe" else int(newwords) * 0.8) + (int(highfuzzy) * 0.4) + (int(lowfuzzy) * 0.6) + (int(hundredpercent) * 0.25))
        
        #Checking input validity
        if lspname == "none":
            flash("Please select an LSP!")
            return redirect("/add_project")
        if  accountname == "none":
            flash("Please select an account!")
            return redirect("/add_project")
        if tasktype == "none":
            flash("Please select a task type!")
            return redirect("/add_project")
        if not projectname:
            flash("Please enter a project name!")
            return redirect("/add_project")
        if not date:
            flash("Please select a date!")
            return redirect("/add_project")
        if not time:
            flash("Please select a time!")
            return redirect("/add_project")
        for num in [newwords, highfuzzy, lowfuzzy, hundredpercent, hourlywork]:
            try:
                val = int(num)
                if val < 0:
                    flash("Please enter a valid number!")
                    return redirect("/add_project")
            except ValueError:
                flash("Please enter a valid number!")
                return redirect("/add_project")
        db.execute("INSERT INTO projects (user_id, lsp_name, account_name, project_name, date_time, task_type, new_words, high_fuzzy, low_fuzzy, hundred_percent, hourlywork, weighted_words, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, lspname, accountname, projectname, date_time, tasktype, newwords, highfuzzy, lowfuzzy, hundredpercent, hourlywork, weighted_words, 'no')
        flash("Project added!")
        return redirect("/")
    else:
        lsps = db.execute("SELECT lsp_name FROM  lsps WHERE user_id = ?", user_id)
        accounts = db.execute("SELECT account_name FROM  accounts WHERE user_id = ?", user_id)
        if not lsps or not accounts:
            flash("Add some LSPs/accounts first!")
            return render_template("add_project.html", lsps=lsps, accounts=accounts, today=today)
        else:
            return render_template("add_project.html", lsps=lsps, accounts=accounts, today=today)

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

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    project_id = request.form.get("project_id")
    user_id = request.form.get("user_id")
    if project_id and int(user_id) == session["user_id"]:
        db.execute("DELETE FROM projects WHERE id = ? AND user_id = ?", project_id, user_id)
        flash("Project deleted successfully!")
    else:
        flash("Project could not be deleted!")

    return redirect("/")

@app.route("/complete", methods=["POST"])
@login_required
def complete():
    project_id = request.form.get("project_id")
    user_id = request.form.get("user_id")
    if project_id and int(user_id) == session["user_id"]:
        db.execute("UPDATE projects SET completed = ? WHERE id = ? AND user_id = ?", "yes", project_id, user_id)
        flash("Project successfully marked as done!")
    else:
        flash("Project could not be marked as done!")

    return redirect("/")

@app.route("/sort")
@login_required
def sort():
    criteria = request.args.get("sort")
    direction = request.args.get("direction")
    user_id = session["user_id"]
    if criteria == "none":
        flash("No sorting criteria selected!")
        return redirect("/")
    else:
        if criteria == "weighted_words":
            projects = db.execute("SELECT * FROM projects WHERE user_id = ?  AND completed = ?" + sorting(criteria, direction, "hourlywork", direction), user_id, 'no')
        else:
            projects = db.execute("SELECT * FROM projects WHERE user_id = ?  AND completed = ?" + sorting(criteria, direction), user_id, 'no')
        
    return render_template("index.html", projects=projects)
        
@app.route("/edit_project", methods=["GET", "POST"])
@login_required
def edit_project():
    if request.method == "POST":
        # Storing form data into variables
        projectId = request.form.get("project_id")
        lspname = request.form.get("lspname")
        accountname = request.form.get("accountname")
        projectname = request.form.get("projectname")
        date = request.form.get("date")
        time = request.form.get("time")
        date_time = f"{date} {time}"
        tasktype  = request.form.get("tasktype")     
        newwords = request.form.get("newwords")
        highfuzzy = request.form.get("highfuzzy")
        lowfuzzy = request.form.get("lowfuzzy")
        hundredpercent = request.form.get("hundredpercent")
        hourlywork = request.form.get("hourlywork")

        if tasktype == "editing":
            weighted_words = int(newwords) + int(highfuzzy) + int(lowfuzzy) + int(hundredpercent)
        else:
            weighted_words = round((int(newwords) if tasktype != "mtpe" else int(newwords) * 0.8) + (int(highfuzzy) * 0.4) + (int(lowfuzzy) * 0.6) + (int(hundredpercent) * 0.25))
        
        #Checking input validity
        if lspname == "none":
            flash("Please select an LSP!")
            return redirect("/add_project")
        if  accountname == "none":
            flash("Please select an account!")
            return redirect("/add_project")
        if tasktype == "none":
            flash("Please select a task type!")
            return redirect("/add_project")
        if not projectname:
            flash("Please enter a project name!")
            return redirect("/add_project")
        if not date:
            flash("Please select a date!")
            return redirect("/add_project")
        if not time:
            flash("Please select a time!")
            return redirect("/add_project")
        for num in [newwords, highfuzzy, lowfuzzy, hundredpercent, hourlywork]:
            try:
                val = int(num)
                if val < 0:
                    flash("Please enter a valid number!")
                    return redirect("/add_project")
            except ValueError:
                flash("Please enter a valid number!")
                return redirect("/add_project")
        db.execute("UPDATE projects SET lsp_name = ?, account_name = ?, project_name = ?, date_time = ?, task_type = ?, new_words = ?, high_fuzzy = ?, low_fuzzy = ?, hundred_percent = ?, hourlywork = ?, weighted_words = ?, completed = ? WHERE id = ?", lspname, accountname, projectname, date_time, tasktype, newwords, highfuzzy, lowfuzzy, hundredpercent, hourlywork, weighted_words, 'no', projectId)
        flash("Project edited!")
        return redirect("/")
    else:
        user_id = session["user_id"]
        project_id = request.args.get("project_id")
        project = db.execute("SELECT * FROM projects WHERE user_id = ? AND id = ?", user_id, project_id)[0]
        date, time = project["date_time"].split(" ")
        lsps = db.execute("SELECT lsp_name FROM  lsps WHERE user_id = ?", user_id)
        accounts = db.execute("SELECT account_name FROM  accounts WHERE user_id = ?", user_id)
        if project:
            return render_template("edit_project.html", lsps=lsps, accounts=accounts, date=date, time=time, project=project)
        else:
            flash("Cannot edit this project!")
            return redirect("/")

