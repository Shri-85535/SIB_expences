from modules import * #Importing classes from modules.py
from flask import Flask, jsonify, request, url_for, abort, g 
from flask_httpauth import HTTPBasicAuth  #Flask-HTTPAuth is a simple extension that simplifies the use of HTTP authentication with Flask routes.
#This class handles HTTP Basic authentication for Flask routes. 



auth = HTTPBasicAuth() 

@auth.verify_password
def verify_password(username, password):
    print ("Looking for user %s" % username)
    user = db.session.query(Users).filter_by(username = username).first()
    if not user: 
        print ("User not found")
        return False
    elif not user.verify_password(password):
        print ("Unable to verify password")
        return False
    else:
        g.user = user
        return True

#endpoint to create new user
@app.route('/users', methods=['POST'])
def new_user():
    username = request.json['username']
    password = request.json['password']
    if username is None or password is None:
        print("missing arguments!")
        abort(400)
        
    user = db.session.query(Users).filter_by(username = username).first()
    if user is not None:
        print ("Existing User")
        return jsonify({'message':'user already exists'}), 200
    
    user = Users(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify ({"username":user.username}), 201

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

#On this part we define endpoint to create new detail.
#First we set the route to “/sibexp” and set HTTP methods to POST.
#After set the route and methods we define function that will executed if we access this endpoint.
#On this function first we get Date, Ration and Vegetables from request data.
#After that we create new_detail using data from request data.
#Last we add new_detail to data base and show new_detail in JSON form as response.

#endpoint to show all details
@app.route('/', methods=['GET'])
@app.route('/sibexp', methods=['GET'])
@auth.login_required
def getall_exp():
    alldetails = DailyExpences.query.all()
    result = all_details.dump(alldetails)
    return jsonify(result.data)

#On this part we define endpoint to get list of all details and show the result as JSON response.

    
#this is main program
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=8080)

#***https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12***
