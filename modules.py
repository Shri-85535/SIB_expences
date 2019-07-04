import pymysql 
pymysql.install_as_MySQLdb() '''PyMySQL and MySQLdb are both database connectors for Python, libraries to enable Python programs to talk to a MySQL server.'''
from flask import Flask, jsonify, request, abort, g '''http://flask.pocoo.org/docs/1.0/appcontext/'''
from flask_sqlalchemy import SQLAlchemy '''Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy. SQLAlchemy is a well-regarded database toolkit and object-relational mapper (ORM) implementation written in Python.'''
from flask_marshmallow import Marshmallow '''***'''
from passlib.apps import custom_app_context as pwd_context '''Passlib is a password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms, as well as a framework for managing existing password hashes.'''

app = Flask(__name__) '''Flask constructor takes the name of current module (__name__) as argument. '''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akash:Myoxyblue35!@localhost/dailyexp' '''The database URI(Uniform Resource Identifier) that should be used for the connection. '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True '''***'''

db=SQLAlchemy(app) 
ma=Marshmallow(app) '''On this part we binding SQLAlchemy and Marshmallow into our flask application.'''


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), index=True)
    password_hash = db.Column(db.String(150))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
'''After import SQLAlchemy and bind it to our flask app, we can declare our models.
Here we declare model called User and defined its field with it’s properties.'''

class DailyExpences(db.Model):
    __tablename__ = 'DailyExpences'
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=False)
    Ration =db.Column(db.Integer, nullable=False) #, NCHAR(8425)
    Vegetables =db.Column(db.Integer, nullable=False)
    
    def __init__(self, Date, Ration, Vegetables):
        self.Date = Date
        self.Ration = Ration
        self.Vegetables = Vegetables

class details_schema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('Date','Ration','Vegetables')

db.create_all()
details = details_schema()
all_details = details_schema(many=True)
