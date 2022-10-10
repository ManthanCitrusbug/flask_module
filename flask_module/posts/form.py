from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField


class AddPost(FlaskForm):
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png']), validators.DataRequired()])
    caption = StringField("Caption", validators=[validators.DataRequired()])
    submit = SubmitField("Add Post")
    
    
class Comment(FlaskForm):
    comment = TextAreaField("Comment")
    submit = SubmitField("Add Comment")
