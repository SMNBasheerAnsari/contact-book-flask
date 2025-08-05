from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    phone= db.Column(db.String(10),nullable=False)
    email=db.Column(db.String(50))
    address=db.Column(db.String(200))
    dob=db.Column(db.String(20))
    
class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), unique=True, nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)
    role=db.Column(db.String(50), default='user') # roles: user, admin, super_admin