from flask import render_template
from flask_module import app, request

@app.errorhandler(401)
def authentication_error(e):
    return render_template("error_pages/authentication_error.html")