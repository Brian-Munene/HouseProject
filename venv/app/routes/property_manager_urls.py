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
@app.route('/SinglePropertyManager/<public_id>')
def single_property_manager(public_id):
    manager = PropertyManager.query.filter_by(public_id=public_id).first()
    if not manager:
        return jsonify({'message': 'Not a property manager'}), 400
    manager_name = manager.first_name + ' ' + manager.last_name
    manager_dict = {
        'manager_name': manager_name,
        'manager_public_id': manager.public_id,
        'email': manager.email,
        'phone': manager.phone
    }
    return jsonify(manager_dict), 200
