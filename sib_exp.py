from modules import app, Users, DailyExpences, details_schema
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
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

#endpoint to show all details
@app.route('/', methods=['GET'])
@app.route('/sibexp', methods=['GET'])
@auth.login_required
def getall_exp():
    alldetails = DailyExpences.query.all()
    result = all_details.dump(alldetails)
    return jsonify(result.data)
    
#this is main program
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=8080)
