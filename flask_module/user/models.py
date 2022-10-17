from email.policy import default
from flask_module import login_manager, db
from flask_login import UserMixin

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
    role = db.relationship("Role", backref="user", lazy=True, cascade = "all, delete, delete-orphan", )
    
    def __repr__(self):
        return f"<User ({self.username})>"
    
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __repr__(self):
        return f"<User ({self.name})>"