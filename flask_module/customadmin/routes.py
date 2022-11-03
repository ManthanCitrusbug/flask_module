from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_module import bcrypt
from flask_module.user.models import User, Role
from flask_module.posts.models import *
from flask_login import current_user, login_user, logout_user
from flask_module.user.forms import LoginForm
from .utiles import login_required

customadmin = Blueprint("customadmin", __name__, url_prefix='/customadmin')

@customadmin.route("/", methods=["POST", "GET"])
@customadmin.route("/login", methods=["POST", "GET"])
def login(): 
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            roles = Role.query.filter(Role.name.in_(["Admin", "Superuser"])).all()
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role in roles:
                login_user(user)
                return redirect(url_for("customadmin.dashboard", username=user.username))
            else:
                flash("User is not able to login.", "danger")
    return render_template("customadmin/login.html", form=form)


@customadmin.route("/dashboard/<string:username>")
@login_required
def dashboard(username):
    users = User.query.filter(User.id != current_user.id)
    return render_template("customadmin/dashboard.html", users=users)


@customadmin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("customadmin.login"))