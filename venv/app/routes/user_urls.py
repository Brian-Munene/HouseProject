from flask import Flask, url_for, session, g, logging, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.user import Token
from database.block import Tenant
from database.block import Caretaker
from database.block import Landlord
from database.block import PropertyManager

auth = HTTPBasicAuth()


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
        category = request_json.get('category')
        first_name = request_json.get('first_name')
        last_name = request_json.get('last_name')
        phone = request_json.get('PhoneNumber')
        if email is None or password is None or category is None:
            return "Fill all details", 400   # missing arguments
        if User.query.filter_by(email=email).first() is not None:
            return "User exists", 400   # existing user
        if category == 'tenant':
            tenant = Tenant(first_name, last_name, email, phone)
            db.session.add(tenant)
            db.session.commit()

            account_status = 3
            user = User(email, category, account_status)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Property manager account has been created.",
                               'email': user.email,
                               'account_status': 'active'}
            return jsonify(response_object), 201
        elif category == 'landlord':
            landlord = Landlord(first_name, last_name, email, phone)
            db.session.add(landlord)
            db.session.commit()

            account_status = 3
            user = User(email, category, account_status)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Property manager account has been created.",
                               'email': user.email,
                               'account_status': 'active'}
            return jsonify(response_object), 201
        elif category == 'caretaker':
            caretaker = Caretaker(first_name, last_name, email, phone)
            db.session.add(caretaker)
            db.session.commit()

            account_status = 3
            user = User(email, category, account_status)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Property manager account has been created.",
                               'email': user.email,
                               'account_status': 'active'}
            return jsonify(response_object), 201
        elif category == 'property manager':
            manager = PropertyManager(first_name, last_name, email, phone)
            db.session.add(manager)
            db.session.commit()

            account_status = 3
            user = User(email, category, account_status)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Property manager account has been created.",
                               'email': user.email,
                               'account_status': 'active'}
            return jsonify(response_object), 201
        else:
            return jsonify({'error': 'Not a valid category'})
    return "Invalid Method", 400


#Login Existing user
@app.route('/login', methods=['POST'])
def login():
    try:
        request_json = request.get_json()

        email = request_json.get('email')
        password = request_json.get('password')
        if email is None or password is None:
            return "Missing arguments", 400   # missing arguments

        user = User.query.filter_by(email=email, account_status=3).first()
        if user and user.verify_password(password):
            auth_token = user.encode_auth_token(user.user_id)
            if auth_token:
                app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
                response_object = {
                    'message': 'Successfully Logged in.',
                    'status': 'success',
                    'public_id': user.user_id,
                    'user_type': user.category,
                    'email': user.email
                }
                return jsonify(response_object), 200
            else:
                app.logger.warning('{0} tried to log in at {1}'.format(email, datetime.now()))
                response_object = {
                    'message': 'Incorrect username or password'
                }
                return jsonify(response_object), 422
        else:
            app.logger.warning('{0} tried to log in at {1}'.format(email, datetime.now()))

            response_object = {
                'message': 'Incorrect username or password'
            }
            return jsonify(response_object), 422


    except(Exception, NameError, TypeError, RuntimeError, ValueError) as identifier:
        response_object = {
            'status': str(identifier),
            'message': 'Try again @login',
            'user': email
        }
        return jsonify(response_object), 500
    except NameError as name_identifier:
        response_object = {
            'status': str(name_identifier),
            'message': 'Try again @login',
            'error': 'Name',
            'username': email
        }
        return jsonify(response_object), 500
    except TypeError as type_identifier:
        response_object = {
            'status': str(type_identifier),
            'message': 'Try again @login',
            'error': 'Type',
            'username': email
        }
        return jsonify(response_object), 500
    except RuntimeError as run_identifier:
        response_object = {
            'status': str(run_identifier),
            'message': 'Try again @login',
            'error': 'Runtime',
            'username': email
        }
        return jsonify(response_object), 500
    except ValueError as val_identifier:
        response_object = {
            'status': str(val_identifier),
            'message': 'Try again @login',
            'error': 'Value',
            'username': email
        }
        return jsonify(response_object), 500
    except Exception as exc_identifier:
        response_object = {
            'status': str(exc_identifier),
            'message': 'Try again @login',
            'error': 'Exception',
            'username': email
        }
        return jsonify(response_object), 500


#View all users
@app.route('/users')
def users():
    users = User.query.filter_by(account_status=3).all()
    usersList = []
    for user in users:
        users_dict = {
                'email': user.email,
                'category': user.category,
                'account_status': 'Active'
                }
        usersList.append(users_dict)
    return jsonify({'data': usersList})
    

#View a single user

@app.route('/user/<id>/')
def user(id):

    user = User.query.get(id)
    if user.account_status == 3:
        status = 'Active'
        user_dict = {
            'email': user.email,
            'category': user.category,
            'account_status': status
        }
        return jsonify({'data': user_dict})
    else:
        return jsonify({'message': 'The account is inactive'}), 500


#Delete a user


@app.route('/deleteuser', methods=['POST', 'GET'])
def delete_user():
    if request.method == 'POST':
        request_json = request.get_json()
        email = request_json.get('email')
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()

        return 'The user has been deleted!', 200
    return 'Invalid Method', 400


#Update  username

@app.route('/updateuser', methods=['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        request_json = request.get_json()
        
        current_email = request_json.get('email')
        new_email = request_json.get('new_email')
        category = request_json.get('category')
        
        user = User.query.filter_by(email=current_email, account_status=3).first()
        if new_email and category:
            user.email = new_email
            db.session.flush()
            user.category = category
            db.session.commit()
            return "Email and Category have been changed", 200
        elif category:
            user.category = category
            db.session.commit()
            return 'The category has been changed', 200
        elif new_email:
            user.email = new_email
            db.session.commit()
            return 'Email updated!', 200
    return 'Invalid Method', 400


@app.route('/SingleCategoryUser/<string:category>/')
def single_category_user(category):
    users = User.query.filter_by(category=category, account_status=3)
    usersList = []
    for user in users:
        users_dict = {
            'email': user.email,
            'category': user.category,
            'account_status': 'Active'
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
            'category': user.category,
            'email': user.email
        }
        return jsonify({'data': user_dict})


