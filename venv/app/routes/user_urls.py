from flask import Flask, url_for, session, g, logging, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
import uuid
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User

from database.block import Tenant
from database.block import Caretaker
from database.block import Landlord
from database.block import PropertyManager
from database.block import Lease
from database.unit import Unit
from database.block import Status
from database.block import Property
from database.block import Debt
from database.block import Statement
from database.block import PaymentType

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
        user_public_id = str(uuid.uuid4())
        status_active = Status.query.filter_by(status_code=3).first()
        account_status = status_active.status_meaning
        if email is None or password is None or category is None or first_name is None or last_name is None or phone is None:
            return jsonify({'message': 'Fill all details'}), 400   # missing arguments
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'message': 'User exists'}), 400   # existing user
        if category == 'tenant':
            if Tenant.query.filter_by(phone=phone).first():
                return jsonify({'message': 'Phone number exists.'}), 400
            unit_id = request_json.get('unit_id')
            lease_begin_date = request_json.get('lease_begin_date')
            lease_end_date = request_json.get('lease_end_date')
            lease_amount = request_json.get('lease_amount')
            promises = request_json.get('promises')
            service_charges = request_json.get('service_charges')
            notes = request_json.get('notes')
            lease_public_id = str(uuid.uuid4())
            lease_status = status_active.status_meaning
            payment_interval = request_json.get('payment_interval')
            if not Unit.query.filter_by(unit_id=unit_id, unit_status='Empty').first():
                return jsonify({'message': 'Unit unavailable'})
            user = User(email, category, account_status, user_public_id)
            user.hash_password(password)
            db.session.add(user)
            db.session.flush()
            tenant_public_id = str(uuid.uuid4())
            tenant = Tenant(first_name, last_name, email, phone, tenant_public_id)
            db.session.add(tenant)
            db.session.flush()
            lease = Lease(tenant.tenant_id, unit_id, lease_begin_date, lease_end_date, lease_amount, promises, service_charges, notes,
                          lease_status,
                          payment_interval, lease_public_id)
            db.session.add(lease)
            db.session.flush()
            total_lease_amount = lease.lease_amount + lease.service_charges
            paid_amount = 0
            status = Status.query.filter_by(status_code=10).first()
            debt_status = status.status_meaning
            debt_public_id = str(uuid.uuid4())
            debt_date = lease_begin_date
            debt = Debt(total_lease_amount, paid_amount, debt_status, debt_date, lease.lease_id, debt_public_id)
            db.session.add(debt)
            db.session.flush()
            tenant_name = tenant.first_name + ' ' + tenant.last_name
            transaction_amount = total_lease_amount
            net_amount = total_lease_amount
            statement_public_id = str(uuid.uuid4())
            transaction_type = PaymentType.query.filter_by(type_code='Ty008').first()
            invoice = transaction_type.type_meaning
            statement = Statement(tenant.tenant_id, unit_id, tenant_name, invoice, transaction_amount, net_amount, debt_date, statement_public_id)
            db.session.add(statement)
            db.session.flush()
            unit = Unit.query.get(unit_id)
            status = Status.query.filter_by(status_code=5).first()
            unit.unit_status = status.status_meaning
            db.session.commit()
            response_object = {'message': "Your Tenant account has been created.",
                               'email': user.email,
                               'user_public_id': user.public_id,
                               'account_status': account_status,
                               'lease_begin_date': lease.lease_begin_date,
                               'lease_end_date': lease.lease_end_date,
                               'lease_amount': lease.lease_amount,
                               'unit_number': unit.unit_number,
                               'lease_status': account_status,
                               'unit_status': unit.unit_status,
                               'service_charges': lease.service_charges,
                               'payment_interval': lease.payment_interval,
                               'total_lease_amount': str(total_lease_amount)
                            }
            return jsonify(response_object), 201
        elif category == 'landlord':
            if Landlord.query.filter_by(phone=phone).first():
                return jsonify({'message': 'Phone number exists.'}), 400
            landlord_public_id = str(uuid.uuid4())
            landlord = Landlord(first_name, last_name, email, phone, landlord_public_id)
            db.session.add(landlord)
            db.session.commit()
            user = User(email, category, account_status, user_public_id)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Landlord account has been created.",
                               'email': user.email,
                               'public_id': user.public_id,
                               'account_status': account_status,
                               'landlord_public_id': landlord.public_id
                               }
            return jsonify(response_object), 201
        elif category == 'caretaker':
            if Caretaker.query.filter_by(phone=phone).first():
                return jsonify({'message': 'Phone number exists.'}), 400
            property_public_id = request_json.get('property_public_id')
            property = Property.query.filter_by(public_id=property_public_id).first()
            caretaker_public_id = str(uuid.uuid4())
            caretaker = Caretaker(property.property_id, first_name, last_name, email, phone, caretaker_public_id)
            db.session.add(caretaker)
            db.session.commit()
            user = User(email, category, account_status, user_public_id)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Caretaker account has been created.",
                               'email': user.email,
                               'account_status': account_status,
                               'public_id': user.public_id}
            return jsonify(response_object), 201
        elif category == 'property manager':
            if PropertyManager.query.filter_by(phone=phone).first():
                return jsonify({'message': 'Phone number exists.'}), 400
            manager_public_id = str(uuid.uuid4())
            manager = PropertyManager(first_name, last_name, email, phone, manager_public_id)
            db.session.add(manager)
            db.session.commit()
            user = User(email, category, account_status, user_public_id)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            response_object = {'message': "Your Property manager account has been created.",
                               'email': user.email,
                               'account_status': account_status,
                               'public_id': user.public_id}
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
        user = User.query.filter_by(email=email, account_status='Active').first()
        if user and user.verify_password(password):
	        if user.category == 'tenant':
		        tenant = Tenant.query.filter_by(email=email).first()
		        lease = Lease.query.filter_by(tenant_id=tenant.tenant_id).first()
		        app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
		        response_object = {
			        'message': 'Successfully Logged in.',
			        'status': 'success',
			        'public_id': user.public_id,
			        'user_type': user.category,
			        'firstname': tenant.first_name,
			        'lastname': tenant.last_name,
			        'email': user.email,
			        'unit_id': lease.unit_id,
			        'tenant_id': lease.tenant_id
		        }
		        return jsonify(response_object), 200
	        elif user.category == 'landlord':
		        landlord = Landlord.query.filter_by(email=email).first()
		        app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
		        response_object = {
			        'message': 'Successfully Logged in.',
			        'status': 'success',
			        'public_id': user.public_id,
			        'user_type': user.category,
			        'firstname': landlord.first_name,
			        'lastname': landlord.last_name,
			        'email': user.email
		        }
		        return jsonify(response_object), 200
	        elif user.category == 'caretaker':
		        caretaker = Caretaker.query.filter_by(email=email).first()
		        app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
		        response_object = {
			        'message': 'Successfully Logged in.',
			        'status': 'success',
			        'public_id': user.public_id,
			        'user_type': user.category,
			        'firstname': caretaker.first_name,
			        'lastname': caretaker.last_name,
			        'email': user.email
		        }
		        return jsonify(response_object), 200
	        elif user.category == "property manager":
		        manager = PropertyManager.query.filter_by(email=email).first()
		        app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
		        response_object = {
			        'message': 'Successfully Logged in.',
			        'status': 'success',
			        'public_id': user.public_id,
			        'user_type': user.category,
			        'firstname': manager.first_name,
			        'lastname': manager.last_name,
			        'email': user.email
		        }
		        return jsonify(response_object), 200
	        else:
		        return jsonify({'message': 'User details are unavailable'})
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
    status_active = Status.query.filter_by(status_code=3).first()
    users = User.query.filter_by(account_status=status_active.status_meaning).all()
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

@app.route('/user/<public_id>/')
def user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if user.account_status == 'Active':
        user_dict = {
            'email': user.email,
            'category': user.category,
            'account_status': user.account_status
        }
        return jsonify({'data': user_dict})
    else:
        return jsonify({'message': 'The account is inactive'}), 500


#Delete a user


@app.route('/DeleteUser/<public_id>')
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    db.session.delete(user)
    db.session.commit()
    return 'The user has been deleted!', 200


#Update  username

@app.route('/UpdateUser/<public_id>', methods=['POST', 'GET'])
def update_user(public_id):
    if request.method == 'POST':
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'No such user'}), 400
        request_json = request.get_json()
        current_email = user.email
        new_email = request_json.get('new_email')
        
        user = User.query.filter_by(email=current_email, account_status=3).first()
        if new_email:
            if user.category == 'tenant':
                tenant = Tenant.query.filter_by(email=current_email).first()
                tenant.email = new_email
                db.session.flush()
                user.email = new_email
                db.session.commit()
                response_object = {'message': 'Email updated!',
                                   'from': current_email,
                                   'to': user.email
                                   }
                return jsonify(response_object), 200
            elif user.category == 'caretaker':
                caretaker = Caretaker.query.filter_by(email=current_email).first()
                caretaker.email = new_email
                db.session.flush()
                user.email = new_email
                db.session.commit()
                response_object = {'message': 'Email updated!',
                                'from': current_email,
                                'to':user.email
                                   }
                return jsonify(response_object), 200
            elif user.category == 'property manager':
                manager = PropertyManager.query.filter_by(email=current_email).first()
                manager.email = new_email
                db.session.flush()
                user.email = new_email
                db.session.commit()
                response_object = {'message': 'Email updated!',
                                   'from': current_email,
                                   'to': user.email
                                   }
                return jsonify(response_object), 200
            elif user.category == 'landlord':
                landlord = Landlord.query.filter_by(email=current_email).first()
                landlord.email = new_email
                db.session.flush()
                user.email = new_email
                db.session.commit()
                response_object = {'message': 'Email updated!',
                                   'from': current_email,
                                   'to': user.email
                                   }
                return jsonify(response_object), 200

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
            # blacklist_token = Token(token=0) #blacklisted token
            try:
                #insert the token
                # db.session.add(blacklist_token)
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


