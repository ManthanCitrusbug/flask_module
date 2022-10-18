from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e670ea4ac75d3720402ec47951f08494'
db_path = os.path.join(os.path.dirname(__file__), 'flask_module.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from flask_module.api.routes import *
from flask_module.user.routes import user
from flask_module.posts.routes import post
from flask_module.customadmin.routes import customadmin
from flask_module.error_handlers import error_handlers

app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(customadmin)
api.add_resource(UsersApi, '/api/users')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserApi, '/api/user/<int:pk>')
api.add_resource(PostsApi, '/api/posts')