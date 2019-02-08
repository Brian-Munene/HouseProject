from flask import Flask, url_for, session, logging, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db
from database.user import User

auth = HTTPBasicAuth()

@app.route('/register', methods = ['GET', 'POST'])  
def register():
    #form = RegisterForm(request.form)
    if request.method == 'POST':
        request_json = request.get_json()

        firstname = request_json.get('firstname')
        lastname = request_json.get('lastname')
        username = request_json.get('username')
        password = request_json.get('password')
        category = request_json.get('category')

        if firstname is None or lastname is None or username is None or password is None or category is None:
            abort(400) #missing arguments
        if User.query.filter_by(username = username).first() is not None:
            abort(400)#existing user
        user.hash_password(password)
        user = User(firstname, lastname, username, category)
        db.session.add(user)
        db.session.commit()

        return jsonify({'username':user.username }), 201, {'Location': url_for('get_user', id =  user.user_id, external = True)}
    return("Invalid Method", 400)

#Login Existing user
@app.route('/login', methods=['POST'])
@auth.verify_password
def login():
    request_json = request.get_json()
    
    username = request_json.get('username')
    password = request_json.get('password')
    if username is None or password is None:
        abort(400)#missing arguments
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user =  user
    return ("You have been logged in", 201)
    


#View all users
@app.route('/users')
def users():
    users = User.query.all()

    usersList = []
    for user in users:
        users_dict = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'category': user.category
                }
        usersList.append(users_dict)
    return jsonify({'data' :usersList})
    

#View a single user

@app.route('/user/<string:id>/')    
def user(id):
    user = User.query.get(id)
    user_dict = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'category':user.category
                }
    return jsonify({'data' :user_dict})

#Delete a user

@app.route('/deleteuser', methods = ['POST', 'GET'])
def delete_user():
    if request.method =='POST':
        request_json = request.get_json()
        username = request_json.get('username')
        user = User.query.filter_by(username = username).first()
        db.session.delete(user)
        db.session.commit()

        return('The user has been deleted!', 'success')
    return ('Invalid Method')

#Update  username

@app.route('/updateuser', methods = ['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        request_json = request.get_json()
        
        current_username = request_json.get('username')
        firstname = request_json.get('firstname')
        lastname = request_json.get('lastname')
        new_username = request_json.get('new_username')
        category = request_json.get('category')
        
        user = User.query.filter_by(username = current_username).first()
        
        if firstname and lastname and category and new_username: 
            user.firstname = firstname 
            db.session.flush() 
            user.lastname = lastname 
            db.session.flush() 
            user.username = new_username 
            db.session.flush() 
            user.category = category 
            db.session.commit() 
            return("Firstname, Lastname, Username and Category have been changed", "Success")
        elif firstname and lastname:
            user.firstname = firstname
            db.session.flush()
            user.lastname = lastname
            db.session.commit()
            return("Firstname and lastname have been changed", "Success")
        elif firstname and lastname and category:
            user.firstname = firstname
            db.session.flush()
            user.category = category
            db.session.flush()
            user.lastname = lastname
            db.session.commit()
            return("Firstname, lastname and category have been changed", "Success")
        elif firstname and category:
            user.firstname = firstname
            db.session.flush()
            user.category = category
            db.session.commit()
            return("Firstname and category have been changed", "success")
        elif firstname and new_username:
            user.firstname = firstname
            db.session.flush()
            user.username = new_username
            db.session.commit()
            return("Firstname and Username have been changed", "Success")
        elif lastname and category:
            user.lastname = lastname
            db.session.flush()
            user.category = category
            db.session.commit()
            return("Lastname and Category have been changed", "success")
        elif lastname and new_username and category:
            user.lastname = lastname
            db.session.flush()
            user.username = new_username
            db.session.flush()
            user.category = category
            db.session.commit()
            return("Lastname, Username and Category have been changed", "success")
        elif new_username and category:
            user.username = new_username
            db.session.flush()
            user.category = category
            db.session.commit()
            return("Username and Category have been changed", "success")

        elif firstname:
            user.firstname = firstname
            db.session.commit()
            return ('The firstname has been changed', "success")
        elif lastname:
            user.lastname = lastname
            db.session.commit()
            return ('The lastname has been changed', "success")
        elif category:
            user.category = category
            db.session.commit()
            return('The category has been changed', "Success")
        elif new_username:
            user.username = new_username
            db.session.commit()
            return('Username updated!', 'success')
    return ('Invalid Method')

@app.route('/SingleCategoryUser/<string:category>/')
def single_category_user(category):
    users = User.query.filter_by(category = category)
    usersList = []
    for user in users:
        users_dict = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'category': user.category
                }
        usersList.append(users_dict)
    return jsonify({'data' :usersList}) 
