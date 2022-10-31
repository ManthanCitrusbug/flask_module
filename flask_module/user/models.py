from flask_module import login_manager, db, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
import base64

connected_user = db.Table(
    'connected_user', 
    db.Column('parent_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('children_id', db.Integer, db.ForeignKey('user.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    profile_picture = db.Column(db.String(70), nullable=False, default="defualt_img.jpg")
    password = db.Column(db.String(15), nullable=False)
    like = db.relationship("Likes", backref="user", lazy=True, cascade = "all, delete, delete-orphan", )
    post = db.relationship("Post", backref="user", lazy=True, cascade = "all, delete, delete-orphan", )
    comment = db.relationship("Comments", backref="user", lazy=True, cascade = "all, delete, delete-orphan", )
    following = db.relationship("User",
                    secondary=connected_user,
                    primaryjoin=id==connected_user.c.parent_id,
                    secondaryjoin=id==connected_user.c.children_id,
                    backref="followed_by")
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    
    def __repr__(self):
        return f"<User ({self.username})>"
    
    def generet_reset_password_token(self, expires_sec=300):
        token = URLSafeTimedSerializer(app.config['SECRET_KEY'], expires_sec)
        return token.dumps(self.id, salt="password-reset-token")
    
    @staticmethod
    def verify_password_token(token):
        ser = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = ser.loads(token, salt="password-reset-token", max_age=10)
        except:
            return None
        return User.query.get(user_id)
            
    
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship("User", backref="role")
    
    def __repr__(self):
        return f"<Role ({self.name})>"