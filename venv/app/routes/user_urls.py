from flask import Flask, url_for, session, g, logging, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.user import Token

auth = HTTPBasicAuth()


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        request_json = request.get_json()

        firstname = request_json.get('firstname')
        lastname = request_json.get('lastname')
        username = request_json.get('username')
        password = request_json.get('password')
        category = request_json.get('category')

        if firstname is None or lastname is None or username is None or password is None or category is None:
            return "Fill all details", 400 #missing arguments
        if User.query.filter_by(username=username).first() is not None:
            return "User exists", 400#existing user
        user = User(firstname, lastname, username, category)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'username': user.username}), 201
    return "Invalid Method", 400


#Login Existing user
@app.route('/login', methods=['POST'])
def login():
    try:
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')
        if username is None or password is None:
            return "Missing arguments", 400 #missing arguments

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            auth_token = user.encode_auth_token(user.user_id)
            if auth_token:
                app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
                response_object = {
                    'message': 'Successfully Logged in.',
                    'status': 'success',
                    'public_id': user.user_id,
                    'user_type': user.category,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'username': user.username
                }
                return jsonify(response_object), 200
            else:
                app.logger.warning('{0} tried to log in at {1}'.format(username, datetime.now()))
                response_object = {
                    'message': 'Incorrect username or password'
                }
                return jsonify(response_object), 422
        else:
            app.logger.warning('{0} tried to log in at {1}'.format(username, datetime.now()))

            response_object = {
                    'message': 'Incorrect username or password'
                }
            return jsonify(response_object), 422
    except(Exception, NameError, TypeError, RuntimeError, ValueError) as identifier:
        response_object = {
            'status': str(identifier),
            'message': 'Try again @login',
            'user': username
        }
        return jsonify(response_object), 500
    except NameError as name_identifier:
        response_object = {
            'status': str(name_identifier),
            'message': 'Try again @login',
            'error': 'Name',
            'username': username
        }
        return jsonify(response_object), 500
    except TypeError as type_identifier:
        response_object = {
            'status': str(type_identifier),
            'message': 'Try again @login',
            'error': 'Type',
            'username': username
        }
        return jsonify(response_object), 500
    except RuntimeError as run_identifier:
        response_object = {
            'status': str(run_identifier),
            'message': 'Try again @login',
            'error': 'Runtime',
            'username': username
        }
        return jsonify(response_object), 500
    except ValueError as val_identifier:
        response_object = {
            'status': str(val_identifier),
            'message': 'Try again @login',
            'error': 'Value',
            'username': username
        }
        return jsonify(response_object), 500
    except Exception as exc_identifier:
        response_object = {
            'status': str(exc_identifier),
            'message': 'Try again @login',
            'error': 'Exception',
            'username': username
        }
        return jsonify(response_object), 500


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

@app.route('/user/<id>/')
def user(id):

    user = User.query.get(id)
    user_dict = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'category': user.category
                }
    return jsonify({'data': user_dict})

#Delete a user


@app.route('/deleteuser', methods=['POST', 'GET'])
def delete_user():
    if request.method == 'POST':
        request_json = request.get_json()
        username = request_json.get('username')
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

        return 'The user has been deleted!', 200
    return 'Invalid Method', 400


#Update  username

@app.route('/updateuser', methods=['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        request_json = request.get_json()
        
        current_username = request_json.get('username')
        firstname = request_json.get('firstname')
        lastname = request_json.get('lastname')
        new_username = request_json.get('new_username')
        category = request_json.get('category')
        
        user = User.query.filter_by(username=current_username).first()
        
        if firstname and lastname and category and new_username: 
            user.firstname = firstname 
            db.session.flush() 
            user.lastname = lastname 
            db.session.flush() 
            user.username = new_username 
            db.session.flush() 
            user.category = category 
            db.session.commit() 
            return "Firstname, Lastname, Username and Category have been changed", 200
        elif firstname and lastname:
            user.firstname = firstname
            db.session.flush()
            user.lastname = lastname
            db.session.commit()
            return "Firstname and lastname have been changed", 200
        elif firstname and lastname and category:
            user.firstname = firstname
            db.session.flush()
            user.category = category
            db.session.flush()
            user.lastname = lastname
            db.session.commit()
            return "Firstname, lastname and category have been changed", 200
        elif firstname and category:
            user.firstname = firstname
            db.session.flush()
            user.category = category
            db.session.commit()
            return "Firstname and category have been changed", 200
        elif firstname and new_username:
            user.firstname = firstname
            db.session.flush()
            user.username = new_username
            db.session.commit()
            return "Firstname and Username have been changed", 200
        elif lastname and category:
            user.lastname = lastname
            db.session.flush()
            user.category = category
            db.session.commit()
            return "Lastname and Category have been changed", 200
        elif lastname and new_username and category:
            user.lastname = lastname
            db.session.flush()
            user.username = new_username
            db.session.flush()
            user.category = category
            db.session.commit()
            return "Lastname, Username and Category have been changed", 200
        elif new_username and category:
            user.username = new_username
            db.session.flush()
            user.category = category
            db.session.commit()
            return "Username and Category have been changed", 200

        elif firstname:
            user.firstname = firstname
            db.session.commit()
            return 'The firstname has been changed', 200
        elif lastname:
            user.lastname = lastname
            db.session.commit()
            return 'The lastname has been changed', 200
        elif category:
            user.category = category
            db.session.commit()
            return 'The category has been changed', 200
        elif new_username:
            user.username = new_username
            db.session.commit()
            return 'Username updated!', 200
    return 'Invalid Method', 400


@app.route('/SingleCategoryUser/<string:category>/')
def single_category_user(category):
    users = User.query.filter_by(category=category)
    usersList = []
    for user in users:
        users_dict = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'category': user.category
                }
        usersList.append(users_dict)
    return jsonify({'data': usersList})


@app.route('/logout')
def logout(self):
    #get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ' '
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            #mark the token as blacklisted
            blacklist_token = Token(token=0) #blacklisted token
            try:
                #insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return jsonify(response_object), 200
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': str(e)
                }
                return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return jsonify(response_object), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return jsonify(response_object), 403


@app.route('/user/single')
def getSingleUser():
    auth_header = request.headers.get('Authentication')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return jsonify(response_object), 401
    else:
        auth_token = ' '
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        user = User.query.filter_by(user_id=resp).first()
        if not user:
            return jsonify({'message': 'No records of that user.'}), 422
        user_dict = {
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'category': user.category,
            'email': user.email
        }
        return jsonify({'data': user_dict})


