from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField
from flask_module.posts.models import *

class CustomadminAddCommentForm(FlaskForm):
    comment = StringField("Comment", validators=[validators.DataRequired()])
    post = SelectField("Post", validators=[validators.DataRequired()], choices=[])
    user = SelectField("User", validators=[validators.DataRequired()], choices=[])
    submit = SubmitField("Add Comment")