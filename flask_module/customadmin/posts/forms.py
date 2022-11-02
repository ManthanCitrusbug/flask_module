from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, SubmitField, SelectField, PasswordField, ValidationError
from flask_module.posts.models import *


class CustomadminAddPostForm(FlaskForm):
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png']), validators.DataRequired()])
    caption = StringField("Caption", validators=[validators.DataRequired()])
    user = SelectField("User", validators=[validators.DataRequired()], choices=[])
    submit = SubmitField("Add Post")
    

class CustomadminEditPostForm(FlaskForm):
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png'])])
    caption = StringField("Caption", validators=[])
    submit = SubmitField("Update Post")