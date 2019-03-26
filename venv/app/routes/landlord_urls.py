from flask import Flask, url_for, session, g, logging, request, json, jsonify
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.block import Landlord
from database.unit import Unit
from database.block import Property
from database.block import PropertyManager


#View all Landlords
@app.route('/ViewLandlords')
def view_landlords():
    landlords = Landlord.query.all()
    landlord_list = []
    for landlord in landlords:
        name = landlord.first_name + ' ' + landlord.last_name
        landlord_dict = {
            'name': name,
            'id': landlord.landlord_id,
            'public_id': landlord.public_id,
            'email': landlord.email,
            'phone': landlord.phone
        }
        landlord_list.append(landlord_dict)
    return jsonify(landlord_list), 200


#View Single Landlord using landlord's public_id
@app.route('/ViewSingleLandlord/<public_id>')
def view_single_landlord(public_id):
    landlord = Landlord.query.filter_by(public_id=public_id).first()
    if not landlord:
        return jsonify({'message': 'Invalid landlord'}), 400
    landlord_dict = {
        'first_name': landlord.first_name,
        'last_name': landlord.last_name,
        'email': landlord.email,
        'phone': landlord.phone
    }
    return jsonify(landlord_dict), 200


#View Property manager Landlords using property manager's user public_id
@app.route('/PropertyManagerLandlords/<public_id>')
def property_manager_landlords(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Invalid User'}), 400
    manager = PropertyManager.query.filter_by(email=user.email).first()
    if not manager:
        return jsonify({'message': 'Invalid Property Manager'}), 400
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if not properties:
        return jsonify({'message': 'No Properties available'}), 400
    landlord_list = []
    for property in properties:
        landlord_dict = {}
        landlord = Landlord.query.filter_by(landlord_id=property.landlord_id).first()
        name = landlord.first_name + ' ' + landlord.last_name
        landlord_dict['name'] = name
        landlord_dict['email'] = landlord.email
        landlord_dict['phone'] = landlord.phone
        landlord_dict['property_name'] = property.property_name
        landlord_dict['public_id'] = landlord.public_id
        landlord_list.append(landlord_dict)
    return jsonify(landlord_list), 200


#Update Landlord_information using landlord's public_id
@app.route('/UpdateLandlord/<public_id>', methods=['POST', 'GET'])
def update_landlord(public_id):
    if request.method == 'GET':
        landlord = Landlord.query.filter_by(public_id=public_id).first()
        if not landlord:
            return jsonify({'message': 'Invalid landlord'}), 400
        landlord_dict = {
            'first_name': landlord.first_name,
            'last_name': landlord.last_name,
            'email': landlord.email,
            'phone': landlord.phone
        }
        return jsonify(landlord_dict), 200
    if request.method == 'POST':
        landlord = Landlord.query.filter_by(public_id=public_id).first()
        if not landlord:
            return jsonify({'message': 'Not a landlord'}), 400
        old_first_name = landlord.first_name
        old_last_name = landlord.last_name
        old_email = landlord.email
        old_phone = landlord.phone
        request_json = request.get_json()
        first_name = request_json.get('first_name')
        last_name = request_json.get('last_name')
        email = request_json.get('email')
        phone = request_json.get('phone')
        response_object = {}
        if not first_name == old_first_name:
            landlord.first_name = first_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_first_name'] = old_first_name
            response_object['new_first_name'] = first_name
        if not last_name == old_last_name:
            landlord.last_name = last_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_last_name'] = old_last_name
            response_object['new_last_name'] = last_name
        if not email == old_email:
            user = User.query.filter_by(email=old_email).first()
            user.email = email
            db.session.flush()
            landlord.email = email
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_email'] = old_email
            response_object['new_email'] = email
        if not phone == old_phone:
            landlord.phone = phone
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_phone'] = old_phone
            response_object['new_phone'] = phone
        return jsonify(response_object), 200

