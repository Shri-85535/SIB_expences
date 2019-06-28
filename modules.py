import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, jsonify, request, url_for, abort, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akash:Myoxyblue35!@localhost/dailyexp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), index=True)
    password_hash = db.Column(db.String(150))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

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
