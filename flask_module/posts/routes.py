from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user
from flask_module.posts.form import AddPost
from flask_module import app, db
from flask_module.posts.models import Post
from sqlalchemy import desc
import os, secrets

post = Blueprint("post", __name__)

@post.route("/posts")
def posts():
    page  = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.created_at)).paginate(per_page=1, page=page)
    return render_template("posts/all_posts.html", posts=posts)


@post.route("/add_post", methods=['POST', 'GET'])
def add_post():
    form = AddPost()
    if request.method == "POST":
        if form.validate_on_submit:
            if form.image.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.image.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.image.data.save(image_path)
                post = Post(image=image_name, caption=form.caption.data, user_id=current_user.id)
            else:
                post = Post(caption=form.caption.data, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("user.profile", username=current_user.username))
    return render_template("posts/add_post.html", form=form)


@post.route("/post_detail/<int:post_id>", methods=['POST', 'GET'])
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template("posts/post_detail.html", post=post)