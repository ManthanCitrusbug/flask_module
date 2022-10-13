from datetime import datetime
from flask_module import db
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(70), nullable=False)
    caption = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comment = db.relationship("Comments", backref="post", lazy=True, cascade = "all, delete, delete-orphan", )
    likes = db.relationship("Likes", backref="post", lazy=True, cascade = "all, delete, delete-orphan", )
    
    def __repr__(self):
        return f"<Post ({self.id})>"
    

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    comment = db.Column(db.String(200), nullable=True)
    
    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)