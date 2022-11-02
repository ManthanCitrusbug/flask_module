from flask_module.customadmin.routes import login_required, superuser_required
from flask import render_template, redirect, url_for, Blueprint
from flask_module.user.models import *
from flask_module.posts.models import Likes

like = Blueprint("like", __name__, url_prefix="/like")

@like.route("/like_list")
@login_required
def like_list():
    # page = request.args.get("page", 1)
    likes = Likes.query.all()
    return render_template("customadmin/likes/likes_list.html", likes=likes)


@like.route("/<int:like_id>/like_detail")
@login_required
def like_detail(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    return render_template("customadmin/likes/like_detail.html", like=like)


@like.route("/<int:like_id>/delete_like")
@login_required
@superuser_required
def delete_like(like_id):
    like = Likes.query.filter_by(id=int(like_id)).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("customadmin.like_list"))