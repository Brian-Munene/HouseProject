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
