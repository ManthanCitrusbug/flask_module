from ast import Delete
from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_login import current_user
from flask_module.posts.form import AddPost
from flask_module import app, db
from flask_module.posts.models import Post, Comments, Likes
from flask_module.user.models import User
import os, secrets






post = Blueprint("post", __name__)

@post.route("/posts")
def posts():
    if "user" in session:
        page  = request.args.get('page', 1, type=int)
        connected_user_id_list = [user.id for user in current_user.following]
        posts = Post.query.filter(Post.user_id.in_(connected_user_id_list)).paginate(per_page=2, page=page)
        return render_template("posts/all_posts.html", posts=posts)
    else:
        return redirect(url_for("user.login"))

@post.route("/add_post", methods=['POST', 'GET'])
def add_post():
    form = AddPost()
    if "user" in session:
        if request.method == "POST":
            if form.validate_on_submit:
                if form.image.data:
                    hex_image = secrets.token_hex(8)
                    f_name, f_ext = os.path.splitext(form.image.data.filename)
                    image_name = hex_image + f_ext
                    image_path = os.path.join(app.root_path, 'static\images', image_name)
                    form.image.data.save(image_path)
                    post = Post(image=image_name, caption=form.caption.data, user_id=current_user.id, )
                else:
                    post = Post(caption=form.caption.data, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for("user.profile", username=current_user.username))
        return render_template("posts/add_post.html", form=form)
    else:
        return redirect(url_for("user.login"))


@post.route("/update_post/<int:post_id>", methods=['POST', 'GET'])
def update_post(post_id):
    form = AddPost()
    post = Post.query.filter_by(id=int(post_id)).first()
    if "user" in session:
        if request.method == 'POST':
            if form.validate_on_submit:
                if form.image.data:
                    hex_image = secrets.token_hex(8)
                    f_name, f_ext = os.path.splitext(form.image.data.filename)
                    image_name = hex_image + f_ext
                    image_path = os.path.join(app.root_path, 'static\images', image_name)
                    form.image.data.save(image_path)
                    post.image = image_name
                post.caption = form.caption.data
                post.user_id = current_user.id
                db.session.commit()
                return redirect(url_for("user.profile", username=current_user.username))
        else:
            form.caption.data = post.caption
            return render_template("posts/update_post.html", post=post, form=form)
    else:
        return redirect(url_for("user.login"))


@post.route("/post_detail/<int:post_id>", methods=['POST', 'GET'])
def post_detail(post_id):
    if "user" in session:
        post = Post.query.filter_by(id=int(post_id)).first()
        comments = Comments.query.filter_by(post_id=int(post_id))
        return render_template("posts/post_detail.html", post=post, comments=comments)
    else:
        return redirect(url_for("user.login"))


@post.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    if "user" in session:
        post = Post.query.filter_by(id=int(post_id)).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("user.profile", username=current_user.username))
    else:
        return redirect(url_for("user.login"))
    
    
@post.route('/add_comment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    comment = Comments(user_id=current_user.id, post_id=post_id , comment=request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("user.profile", username=current_user.username))


@post.route("/like/<int:post_id>", methods=['POST', 'GET'])
def like_a_post(post_id):
    like = Likes(user_id=current_user.id, post_id=int(post_id))
    db.session.add(like)
    db.session.commit()
    return redirect(url_for("post.posts"))


@post.route("/dislike/<int:like_id>", methods=['POST', 'GET'])
def dislike(like_id):
    like = Likes.query.filter_by(id=like_id).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("post.posts")) 