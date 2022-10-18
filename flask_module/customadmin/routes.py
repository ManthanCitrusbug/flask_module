from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_module import db, app, bcrypt
from flask_module.posts.models import Likes
from flask_module.user.models import User, Role
from flask_module.posts.models import *
from flask_login import current_user, login_user, logout_user
from flask_module.user.forms import LoginForm

customadmin = Blueprint("customadmin", __name__)

# ---------------------------------------------------------------------------------
# ------------- Customadmin ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin", methods=["POST", "GET"])
@customadmin.route("/customadmin/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            roles = Role.query.filter(Role.name.in_(["Admin", "Superuser"])).all()
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role in roles:
                login_user(user)
                return redirect(url_for("customadmin.dashboard", username=user.username))
    return render_template("customadmin/login.html", form=form)


@customadmin.route("/customadmin/dashboard/<string:username>")
def dashboard(username):
    users = User.query.filter(User.id != current_user.id)
    return render_template("customadmin/dashboard.html", users=users)


@customadmin.route("/customadmin/logout")
def logout():
    logout_user()
    return redirect(url_for("customadmin.login"))

# ---------------------------------------------------------------------------------
# ------------- Customadmin ---------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------- Customadmin User ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin/<int:user_id>/user_detail")
def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("customadmin/users/user_detail.html", user=user)


@customadmin.route("/customadmin/<int:user_id>/delete_user")
def delete_user(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("customadmin.dashboard", username=current_user.username))

# ---------------------------------------------------------------------------------
# ------------- Customadmin User ---------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------- Customadmin Post ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin/post_list")
def post_list():
    page = request.args.get("page", 1)
    posts = Post.query.paginate(per_page=7, page=int(page))
    return render_template("customadmin/posts/post_list.html", posts=posts)


@customadmin.route("/customadmin/<int:post_id>/post_detail")
def post_detail(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    return render_template("customadmin/posts/post_detail.html", post=post)


@customadmin.route("/customadmin/<int:post_id>/delete_post")
def delete_post(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("customadmin.post_list"))


# ---------------------------------------------------------------------------------
# ------------- Customadmin Post ---------------
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# ------------- Customadmin Like ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin/like_list")
def like_list():
    page = request.args.get("page", 1)
    likes = Likes.query.paginate(per_page=7, page=int(page))
    return render_template("customadmin/likes/likes_list.html", likes=likes)


@customadmin.route("/customadmin/<int:like_id>/like_detail")
def like_detail(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    return render_template("customadmin/likes/like_detail.html", like=like)


@customadmin.route("/customadmin/<int:like_id>/delete_like")
def delete_like(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("customadmin.like_list"))