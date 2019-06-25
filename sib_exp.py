import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akash:Myoxyblue35!@localhost/dailyexp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db=SQLAlchemy(app)
ma=Marshmallow(app)

class DailyExpences(db.Model):
    __tablename__ = 'DailyExpences'
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=True)
    Ration =db.Column(db.Integer) #, NCHAR(8425)
    Vegetables =db.Column(db.Integer)
    
    def __init__(self, Date, Ration, Vegetables):
        self.Date = Date
        self.Ration = Ration

class details_schema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('Date','Ration','Vegetables')

db.create_all()
details = details_schema()
all_details = details_schema(many=True)

#endpoint to create new detail
@app.route('/sibexp', methods=['POST'])
def add_exp():
    Date = request.json['Date']
    Ration = request.json['Ration']
    Vegetables =request.json['Vegetables']
    
    new_detail = DailyExpences(Date,Ration,Vegetables)
    db.session.add(new_detail)
    db.session.commit()
    
    dexp = DailyExpences.query.get(new_detail.id)
    return details.jsonify(dexp)

#endpoint to show all details
@app.route('/sibexp', methods=['GET'])
@app.route('/', methods=['GET'])
def getall_exp():
    alldetails = DailyExpences.query.all()
    result = all_details.dump(alldetails)
    return jsonify(result.data)
    
#this is main program
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=8080)
