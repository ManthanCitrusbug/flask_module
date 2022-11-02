from pickle import TRUE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e670ea4ac75d3720402ec47951f08494'
db_path = os.path.join(os.path.dirname(__file__), 'flask_module.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# # app.config['MAIL_SERVER'] = 'smtp.google.com'
# app.config['MAIL_PORT'] = 465
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
# app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
csrf = CSRFProtect(app)

from flask_module.api.routes import *
from flask_module.user.routes import user
from flask_module.posts.routes import post
from flask_module.customadmin.routes import customadmin
from flask_module.customadmin.users.routes import users
from flask_module.customadmin.posts.routes import post
from flask_module.customadmin.comments.routes import comment
from flask_module.customadmin.likes.routes import like
from flask_module.error_handlers import error_handlers

app.register_blueprint(user)
app.register_blueprint(post)
customadmin.register_blueprint(users)
customadmin.register_blueprint(post)
customadmin.register_blueprint(comment)
customadmin.register_blueprint(like)
app.register_blueprint(customadmin)
api.add_resource(UsersApi, '/api/users')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserApi, '/api/user/<int:pk>')
api.add_resource(PostsApi, '/api/posts')