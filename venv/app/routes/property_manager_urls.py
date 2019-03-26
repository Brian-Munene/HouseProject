from flask import Flask, url_for, session, g, logging, request, json, jsonify
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.block import Caretaker
from database.unit import Unit
from database.block import Property
from database.block import PropertyManager


# View Property managers
@app.route('/PropertyManagers')
def property_managers():
    managers = PropertyManager.query.all()
    if not managers:
        return jsonify({'message': 'No Property Managers available'}), 400
    managers_list = []
    for manager in managers:
        managers_dict = {}
        manager_name = manager.first_name + ' ' + manager.last_name
        managers_dict['manager_name'] = manager_name
        managers_dict['manager_public_id'] = manager.public_id
        managers_dict['email'] = manager.email
        managers_dict['phone'] = manager.phone
        managers_list.append(managers_dict)
    return jsonify(managers_list), 200


#View Single Property Manager
@app.route('/ViewSinglePropertyManager/<public_id>')
def single_property_manager(public_id):
    manager = PropertyManager.query.filter_by(public_id=public_id).first()
    if not manager:
        return jsonify({'message': 'Not a property manager'}), 400
    manager_dict = {
        'first_name': manager.first_name,
        'last_name': manager.last_name,
        'manager_public_id': manager.public_id,
        'email': manager.email,
        'phone': manager.phone
    }
    return jsonify(manager_dict), 200


#Update Landlord_information using manager's public_id
@app.route('/UpdatePropertyManager/<public_id>', methods=['POST', 'GET'])
def update_property_manager(public_id):
    if request.method == 'GET':
        manager = PropertyManager.query.filter_by(public_id=public_id).first()
        if not manager:
            return jsonify({'message': 'Invalid Property Manager'}), 400
        manager_dict = {
            'first_name': manager.first_name,
            'last_name': manager.last_name,
            'email': manager.email,
            'phone': manager.phone
        }
        return jsonify(manager_dict), 200
    if request.method == 'POST':
        manager = PropertyManager.query.filter_by(public_id=public_id).first()
        if not manager:
            return jsonify({'message': 'Not a Property Manager'}), 400
        old_first_name = manager.first_name
        old_last_name = manager.last_name
        old_email = manager.email
        old_phone = manager.phone
        request_json = request.get_json()
        first_name = request_json.get('first_name')
        last_name = request_json.get('last_name')
        email = request_json.get('email')
        phone = request_json.get('phone')
        response_object = {}
        if not first_name == old_first_name:
            manager.first_name = first_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_first_name'] = old_first_name
            response_object['new_first_name'] = first_name
        if not last_name == old_last_name:
            manager.last_name = last_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_last_name'] = old_last_name
            response_object['new_last_name'] = last_name
        if not email == old_email:
            user = User.query.filter_by(email=old_email).first()
            user.email = email
            db.session.flush()
            manager.email = email
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_email'] = old_email
            response_object['new_email'] = email
        if not phone == old_phone:
            manager.phone = phone
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_phone'] = old_phone
            response_object['new_phone'] = phone
        return jsonify(response_object), 200
