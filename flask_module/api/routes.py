from flask_restful import Api, Resource, marshal_with, fields
from flask_module.user.models import *
from flask_module.posts.models import *
from flask_module import app, bcrypt
from flask import request
import random

api = Api(app)

userfields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "profile_picture": fields.String,
}

postfields = {
    "id": fields.Integer,
    "image": fields.String,
    "caption": fields.String,
    "created_at": fields.DateTime,
    "user": fields.Nested(userfields)
}

class UserLogin(Resource):
    # @marshal_with(userfields)
    def post(self):
        responce = request.json
        user = User.query.filter_by(email=responce['email']).first()
        if user and bcrypt.check_password_hash(user.password, responce['password']):
            code = random.choice(range(100000, 999999))

        # qry_users = User.query.all()
        return code


class UsersApi(Resource):
    @marshal_with(userfields)
    def get(self):
        qry_user = User.query.all()
        return qry_user
    
    @marshal_with(userfields)
    def post(self):
        responce = request.json
        user = User(username=responce['username'], email=responce['email'], password=responce['password'])
        db.session.add(user)
        db.session.commit()
        
        qry_user = User.query.all()
        
        return qry_user
    

class UserApi(Resource):
    @marshal_with(userfields)
    def get(self, pk):
        user = User.query.filter_by(id=pk).first()
        return user
    
    @marshal_with(userfields)
    def delete(self, pk):
        user = User.query.filter_by(id=pk).first()
        db.session.delete(user)
        db.session.commit()
        
        qry_user = User.query.all()
        return qry_user
    
    @marshal_with(userfields)
    def put(self, pk):
        responce = request.json
        user = User.query.filter_by(id=pk).first()
        
        user.username = responce['username']
        user.email = responce['email']
        user.password = responce['password']
        
        db.session.commit()
        
        qry_user = User.query.all()
        return qry_user 
    
    
class PostsApi(Resource):
    @marshal_with(postfields)
    def get(self):
        qry_posts = Post.query.all()
        return qry_posts