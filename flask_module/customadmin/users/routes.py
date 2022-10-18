# from flask_module.customadmin.routes import customadmin
# from flask import render_template
# from flask_module.user.models import User


# @customadmin.route("/<int:user_id>/detail")
# def user_detail(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     return render_template("customadmin/users/user_detail.html", user=user)