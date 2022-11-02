from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, SubmitField, SelectField, PasswordField, ValidationError
from flask_module.user.models import User
from flask_module.posts.models import *

class CustomadminAddUserForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(), validators.Length(min=2, max=15)])
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    profile_picture = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=2, max=10)])
    confirm_password = PasswordField("Confirm Password", validators=[validators.DataRequired(), validators.EqualTo("password")])
    role = SelectField("User Role", validators=[validators.DataRequired()], choices=[])
    submit = SubmitField("Add User")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already exist. Please try another.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already exist. Please try another.")


class CustomadminEditUserForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(), validators.Length(min=2, max=15)])
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    profile_picture = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    role = SelectField("User Role", validators=[validators.DataRequired()], choices=[])
    submit = SubmitField("Update User")