from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    # __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #one to many - user to notes
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))  #lower on FK

class User(db.Model, UserMixin):
    #sign up form info
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    #list of all created notes
    notes = db.relationship('Note') #capt on relationship