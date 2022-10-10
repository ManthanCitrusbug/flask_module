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

from flask_module.user.routes import user
from flask_module.posts.routes import post

app.register_blueprint(user)
app.register_blueprint(post)