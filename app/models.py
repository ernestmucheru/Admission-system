from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index =True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    #role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(5000))
    profile_pic_path = db.Column(db.String)
    pass_secure = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    """ pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic") """
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'


class Courses(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key = True)
    institution = db.Column(db.String(150),index =True)
    title = db.Column(db.String(255),index =True)
    description = db.Column(db.String(12255))
    

    