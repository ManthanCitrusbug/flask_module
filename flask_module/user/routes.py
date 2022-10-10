from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_module.user.forms import RegistraionForm, LoginForm
from flask_module.user.models import User
from flask_module.posts.models import Post
from flask_login import current_user, login_user, logout_user
from flask_module import bcrypt, db, app
import secrets, os

user = Blueprint("user", __name__)

# db.drop_all()
# db.create_all()

@user.route("/")
def home():
    # db.drop_all()
    db.create_all()
    return render_template("home.html")


@user.route("/register", methods=["POST", "GET"])
def register():
    form = RegistraionForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if form.profile_picture.data:
            hex_image = secrets.token_hex(8)
            f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
            image_name = hex_image + f_ext
            image_path = os.path.join(app.root_path, 'static\images', image_name)
            form.profile_picture.data.save(image_path)
            user = User(username=form.username.data, email=form.email.data, profile_picture=image_name, password=hashed_password)
        else:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.login"))
    return render_template("user/register.html", form=form)


@user.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("user.profile", username=user.username))
    return render_template("user/login.html", form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@user.route("/profile/<string:username>", methods=["POST", "GET"])
def profile(username):
    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(user_id=user.id)
    return render_template("user/profile.html", user=user, posts=post)


@user.route("/<int:user_id>/update", methods=["POST", "GET"])
def update(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = RegistraionForm()
    if request.method == "POST":
        if form.validate_on_submit:
            if form.profile_picture.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.profile_picture.data.save(image_path)
                user.profile_picture = image_name
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            return redirect(url_for("user.profile", username=user.username))
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.profile_picture.data = user.profile_picture
        form.submit.label.text = "Update Profile"
        return render_template("user/update_profile.html", user=user, form=form)
    

@user.route("/users", methods=['POST', 'GET'])
def users():
    page  = request.args.get('page', 1, type=int)
    users = User.query.filter(User.id != current_user.id).paginate(per_page=1, page=page)
    return render_template("user/all_users.html", users=users)


@user.route("/profile_detail/<string:username>", methods=["POST", "GET"])
def profile_detail(username):
    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(user_id=user.id)
    return render_template("user/profile_detail.html", user=user, posts=post)