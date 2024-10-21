from cs50 import SQL
from flask import flash, redirect, request, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def add_entity(entity_name, table_name, column_name, redirect_route, db):
    user_id = session["user_id"]
    entity_value = request.form.get(entity_name)
    
    # Checking for empty input
    if not entity_value:
        flash("Name field is required!")
        return redirect(redirect_route)
    
    # Checking for duplicate entries
    query = f"SELECT {column_name} FROM {table_name} WHERE LOWER({column_name}) = ? AND user_id = ?"
    if db.execute(query, entity_value.lower(), user_id):
        flash("This name already exists!")
        return redirect(redirect_route)
    
    # Adding to the database
    insert_query = f"INSERT INTO {table_name} (user_id, {column_name}) VALUES (?, ?)"
    db.execute(insert_query, user_id, entity_value)
    
    flash("Successfully added!")
    return redirect("/")