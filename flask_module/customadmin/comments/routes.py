from ..utiles import *
from flask import render_template, redirect, request, url_for, Blueprint
from flask_module.customadmin.comments.forms import *
from flask_module.user.models import *

comment = Blueprint("comment", __name__, url_prefix="/comment")

@comment.route("/add_comment", methods=["POST", "GET"])
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
            return redirect(url_for("customadmin.comment.comments_list"))
    return render_template("customadmin/comments/add_comment.html", form=form)


@comment.route("/<int:comment_id>/comment_update", methods=["POST", "GET"])
@login_required
@superuser_required
def comment_update(comment_id):
    comment_obj = Comments.query.filter_by(id=int(comment_id)).first()
    if request.method == "POST":
        comment = request.form.get("comment")
        comment_obj.comment = comment
        db.session.commit()
        return redirect(url_for('customadmin.comment.comments_list'))
    return render_template("customadmin/comments/update_comment.html", comment=comment_obj)


@comment.route("/comments_list")
@login_required
def comments_list():
    # page = request.args.get("page", 1)
    comments = Comments.query.all()
    return render_template("customadmin/comments/comments_list.html", comments=comments)


@comment.route("/<int:comment_id>/comment_detail")
@login_required
def comment_detail(comment_id):
    comment = Comments.query.filter_by(id=int(comment_id)).first()
    return render_template("customadmin/comments/comment_detail.html", comment=comment)


@comment.route("/<int:comment_id>/delete_comment")
@login_required
@superuser_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=int(comment_id)).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("customadmin.comment.comments_list"))