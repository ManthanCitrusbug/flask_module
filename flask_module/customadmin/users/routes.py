from flask_module.customadmin.routes import login_required, superuser_required
from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import current_user
from flask_module.customadmin.users.forms import *
from flask_module.user.models import *
from flask_module import bcrypt 
import secrets, os

users = Blueprint("users", __name__, url_prefix="/user")

@users.route("/add_user", methods=["POST", "GET"])
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


@users.route("/<int:user_id>/user_update", methods=["POST", "GET"])
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


@users.route("/<int:user_id>/user_detail")
@login_required
def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("customadmin/users/user_detail.html", user=user)


@users.route("/<int:user_id>/delete_user")
@login_required
@superuser_required
def delete_user(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("customadmin.dashboard", username=current_user.username))
