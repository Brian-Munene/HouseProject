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


#View caretakers for a specific property using property's public_id
@app.route('/PropertyCaretakers/<public_id>')
def property_caretaker(public_id):
    property = Property.query.filter_by(public_id=public_id).first()
    if not property:
        return jsonify({'message': 'No such property'}), 400
    caretakers = Caretaker.query.filter_by(property_id=property.property_id).all()
    if not caretakers:
        return jsonify({'message': 'No caretakers'}), 200
    caretaker_list = []
    for caretaker in caretakers:
        name = caretaker.first_name + ' ' + caretaker.last_name
        caretaker_dict = {
            'caretaker_id': caretaker.caretaker_id,
            'public_id': caretaker.public_id,
            'name': name
        }
        caretaker_list.append(caretaker_dict)
    return jsonify(caretaker_list), 200


#View a single caretaker
@app.route('/SingleCaretaker/<public_id>')
def single_caretaker(public_id):
    caretaker = Caretaker.query.filter_by(public_id=public_id).first()
    if not caretaker:
        return jsonify({'message': 'No caretaker'}), 400
    caretaker_name = caretaker.first_name + ' ' + caretaker.last_name
    caretaker_dict = {
        'name': caretaker_name,
        'phone': caretaker.phone,
        'email': caretaker.email,
        'public_id': caretaker.public_id
    }
    return jsonify(caretaker_dict), 200


# PropertyManger caretakers using property manager's user public_id
@app.route('/PropertyManagerCaretakers/<public_id>')
def property_manger_caretakers(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'You are not a  property manger'}), 400
    manager = PropertyManager.query.filter_by(email=user.email).first()
    if not manager:
        return jsonify({'message': 'Invalid manager'}), 400
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if not properties:
        return jsonify({'message': 'No Property available'}), 400
    caretakers_list = []
    for property in properties:
        caretakers = Caretaker.query.filter_by(property_id=property.property_id).all()
        for caretaker in caretakers:
            caretaker_dict = {}
            name = caretaker.first_name + ' ' + caretaker.last_name
            caretaker_dict['name'] = name
            caretaker_dict['email'] = caretaker.email
            caretaker_dict['phone'] = caretaker.phone
            caretaker_dict['public_id'] = caretaker.public_id
            caretakers_list.append(caretaker_dict)
    return jsonify(caretakers_list), 200
