from flask import Flask, session, logging, request, json, jsonify


#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.user import User


@app.route('/InsertUnit', methods=['GET', 'POST'])
def insert_unit():
	if request.method == 'POST':

		request_json = request.get_json()
		block_id = request_json.get('block_id')
		unit_status = 6

		unit = Unit(block_id, unit_status)
		db.session.add(unit)
		db.session.commit()
		response_object = {
			'unit_id': unit.unit_id,
			'block_id': unit.block_id,
			'unit_status': unit.unit_status
		}

		return jsonify(response_object), 201
	return jsonify({'error': 'Invalid Method'})


#View all units
@app.route('/Units')
def units():
	units = Unit.query.all()
	unitsList = []
	for unit in units:
		units_dict = {
				'block_id': unit.block_id,
				'unit_status': unit.unit_status
				}
		unitsList.append(units_dict)

	return jsonify({'data': unitsList})


#View a single unit
@app.route('/Unit/<id>/')
def unit(id):
	unit = Unit.query.get(id)
	unit_dict = {
		'block_id': unit.block_id,
		'unit_status': unit.unit_status
	}
	return jsonify({'data': unit_dict})


#Update  Unit details
@app.route('/UpdateUnit/<id>/', methods=['POST', 'GET'])
def update_unit(id):
	if request.method == 'POST':
		request_json = request.get_json()
		new_status = request_json.get('unit_status')
		unit = Unit.query.get(id)
		unit.unit_status = new_status
		db.session.commit()
		response_object = {
			'Message': 'Unit Status has been updated successfully',
			'block_id': unit.block_id,
			'new_status': unit.unit_status
		}
		return jsonify(response_object), 200


	#Delete a Unit
@app.route('/DeleteUnit/<id>/', methods=['DELETE'])
def delete_unit(id):
		unit = Unit.query.get(id)
		db.session.delete(unit)
		db.session.commit()
		return jsonify({'message': 'The Unit has been deleted!'}), 200

