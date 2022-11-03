from ..utiles import *
from flask import render_template, redirect, request, url_for, Blueprint
from flask_module.customadmin.posts.forms import *
from flask_module.user.models import *
import secrets, os

posts = Blueprint("post", __name__, url_prefix="/post")

@posts.route("/add_post", methods=["POST", "GET"])
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
            return redirect(url_for("customadmin.post.post_list"))
    return render_template("customadmin/posts/add_post.html", form=form)


@posts.route("/<int:post_id>/post_update", methods=["POST", "GET"])
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
            return redirect(url_for("customadmin.post.post_list"))
    else:
        form.caption.data = post.caption
        return render_template("customadmin/posts/update_post.html", form=form, post=post)


@posts.route("/post_list")
@login_required
def post_list():
    posts = Post.query.all()
    return render_template("customadmin/posts/post_list.html", posts=posts)


@posts.route("/<int:post_id>/post_detail")
@login_required
def post_detail(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    return render_template("customadmin/posts/post_detail.html", post=post)


@posts.route("/<int:post_id>/delete_post")
@login_required
@superuser_required
def delete_post(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("customadmin.post.post_list"))