from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_module import db, bcrypt, app
from flask_module.posts.models import Likes
from flask_module.user.models import User, Role
from flask_module.posts.models import *
from flask_login import current_user, login_user, logout_user
from flask_module.user.forms import LoginForm
from flask_module.customadmin.forms import *
from flask_wtf.csrf import CSRFProtect
from functools import wraps
import secrets, os

customadmin = Blueprint("customadmin", __name__)
csrf = CSRFProtect(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):   
        if current_user.is_authenticated is False:
            return redirect(url_for('customadmin.login'))
        return f(*args, **kwargs)
    return decorated_function

def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role.name != "Superuser":
                return redirect(url_for('customadmin.dashboard', username=current_user.username))
        return f(*args, **kwargs)
    return decorated_function
            
    

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
            else:
                flash("User is not able to login.", "danger")
    return render_template("customadmin/login.html", form=form)


@customadmin.route("/customadmin/dashboard/<string:username>")
@login_required
def dashboard(username):
    users = User.query.filter(User.id != current_user.id)
    return render_template("customadmin/dashboard.html", users=users)


@customadmin.route("/customadmin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("customadmin.login"))

# ---------------------------------------------------------------------------------
# ------------- Customadmin ---------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------- Customadmin User ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin/add_user", methods=["POST", "GET"])
@login_required
@superuser_required
def add_user():
    form = CustomadminAddUserForm()
    form.role.choices = [role.name for role in Role.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            role = Role.query.filter_by(name=form.role.data).first()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            if form.profile_picture.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.profile_picture.data.save(image_path)
                user = User(username=form.username.data, email=form.email.data, profile_picture=image_name, password=hashed_password, role_id=role.id)
            else:
                user = User(username=form.username.data, email=form.email.data, password=hashed_password, role_id=role.id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('customadmin.dashboard', username=current_user.username))
    return render_template("customadmin/users/add_user.html", form=form)


@customadmin.route("/customadmin/<int:user_id>/user_update", methods=["POST", "GET"])
@login_required
@superuser_required
def user_update(user_id):
    form = CustomadminEditUserForm()
    user = User.query.filter_by(id=int(user_id)).first()
    form.role.choices = [role.name for role in Role.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            if form.profile_picture.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.profile_picture.data.save(image_path)
                user.profile_picture = image_name
            user.username = form.username.data
            user.email = form.email.data
            role = Role.query.filter_by(name=form.role.data).first()
            user.role = role
            db.session.commit()
            return redirect(url_for("customadmin.dashboard", username=current_user.username))
    else:
        form.username.data = user.username  
        form.email.data = user.email
        form.profile_picture.data = user.profile_picture
        form.role.data = user.role.name
        return render_template("customadmin/users/update_user.html", user=user, form=form)


@customadmin.route("/customadmin/<int:user_id>/user_detail")
@login_required
def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("customadmin/users/user_detail.html", user=user)


@customadmin.route("/customadmin/<int:user_id>/delete_user")
@login_required
@superuser_required
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

@customadmin.route("/customadmin/add_post", methods=["POST", "GET"])
@login_required
@superuser_required
def add_post():
    form = CustomadminAddPostForm()
    form.user.choices = [(user.id, user.username) for user in User.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            print()
            if form.image.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.image.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.image.data.save(image_path)
                post = Post(image=image_name, caption=form.caption.data, user_id=form.user.data)
            else:
                post = Post(caption=form.caption.data, user_id=form.user.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("customadmin.post_list"))
    return render_template("customadmin/posts/add_post.html", form=form)


@customadmin.route("/customadmin/<int:post_id>/post_update", methods=["POST", "GET"])
@login_required
@superuser_required
def post_update(post_id):
    form = CustomadminEditPostForm()
    post = Post.query.filter_by(id=int(post_id)).first()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.image.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.image.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.image.data.save(image_path)
                post.image = image_name
            post.caption = form.caption.data
            db.session.commit()
            return redirect(url_for("customadmin.post_list"))
    else:
        form.caption.data = post.caption
        return render_template("customadmin/posts/update_post.html", form=form, post=post)


@customadmin.route("/customadmin/post_list")
@login_required
def post_list():
    # page = request.args.get("page", 1)
    posts = Post.query.all()
    # posts = Post.query.paginate(per_page=7, page=int(page))
    return render_template("customadmin/posts/post_list.html", posts=posts)


@customadmin.route("/customadmin/<int:post_id>/post_detail")
@login_required
def post_detail(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    return render_template("customadmin/posts/post_detail.html", post=post)


@customadmin.route("/customadmin/<int:post_id>/delete_post")
@login_required
@superuser_required
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
@login_required
def like_list():
    # page = request.args.get("page", 1)
    likes = Likes.query.all()
    return render_template("customadmin/likes/likes_list.html", likes=likes)


@customadmin.route("/customadmin/<int:like_id>/like_detail")
@login_required
def like_detail(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    return render_template("customadmin/likes/like_detail.html", like=like)


@customadmin.route("/customadmin/<int:like_id>/delete_like")
@login_required
@superuser_required
def delete_like(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("customadmin.like_list"))

# ---------------------------------------------------------------------------------
# ------------- Customadmin Like ---------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------- Customadmin Comment ---------------
# ---------------------------------------------------------------------------------

@customadmin.route("/customadmin/add_comment", methods=["POST", "GET"])
@login_required
@superuser_required
def add_comment():
    form = CustomadminAddCommentForm()
    form.post.choices = [(post.id, (post.user.username, post.caption)) for post in Post.query.all()]
    form.user.choices = [(user.id, user.username) for user in User.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            comment = Comments(comment=form.comment.data, user_id=form.user.data, post_id=form.post.data)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("customadmin.comments_list"))
    return render_template("customadmin/comments/add_comment.html", form=form)


@customadmin.route("/customadmin/<int:comment_id>/comment_update", methods=["POST", "GET"])
@login_required
@superuser_required
def comment_update(comment_id):
    comment_obj = Comments.query.filter_by(id=int(comment_id)).first()
    if request.method == "POST":
        comment = request.form.get("comment")
        comment_obj.comment = comment
        db.session.commit()
        return redirect(url_for('customadmin.comments_list'))
    return render_template("customadmin/comments/update_comment.html", comment=comment_obj)


@customadmin.route("/customadmin/comments_list")
@login_required
def comments_list():
    # page = request.args.get("page", 1)
    comments = Comments.query.all()
    return render_template("customadmin/comments/comments_list.html", comments=comments)


@customadmin.route("/customadmin/<int:comment_id>/comment_detail")
@login_required
def comment_detail(comment_id):
    comment = Comments.query.filter_by(id=int(comment_id)).first()
    return render_template("customadmin/comments/comment_detail.html", comment=comment)


@customadmin.route("/customadmin/<int:comment_id>/delete_comment")
@login_required
@superuser_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=int(comment_id)).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("customadmin.comments_list"))