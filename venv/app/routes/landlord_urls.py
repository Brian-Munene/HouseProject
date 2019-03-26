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


#View Single Landlord
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
@app.route('/UpdateLandlord/public_id', methods=['POST'])
def update_landlord(public_id):
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
	if first_name:
		landlord.first_name = first_name
		db.session.commit()
		response_object = {
			'status': 'First Name has been changed',
			'from': old_first_name,
			'to': first_name
		}
		return jsonify(response_object), 200
	if last_name:
		landlord.last_name = last_name
		db.session.commit()
		response_object = {
			'status': 'First Name has been changed',
			'from': old_last_name,
			'to': last_name
		}
		return jsonify(response_object), 200
	if email:
		user = User.query.filter_by(email=email).first()
		user.email = email
		db.session.flush()
		landlord.email = email
		db.session.commit()
		response_object = {
			'status': 'First Name has been changed',
			'from': old_email,
			'to': email
		}
		return jsonify(response_object), 200
	if phone:
		landlord.phone = phone
		db.session.commit()
		response_object = {
			'status': 'First Name has been changed',
			'from': old_phone,
			'to': phone
		}
		return jsonify(response_object), 200
