from flask import Flask, session, logging, request, json, jsonify
import uuid

#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.user import User
#from database.block import Tenant
from database.block import PropertyManager
from database.block import Status
from database.block import Block
from database.block import Tenant
from database.block import Lease


# Register Unit using user public_id
@app.route('/InsertUnit/<public_id>', methods=['GET', 'POST'])
def insert_unit(public_id):
	if request.method == 'POST':
		user = User.query.filter_by(public_id=public_id).first()
		manager = PropertyManager.query.filter_by(email=user.email).first()
		if not manager:
			return jsonify({'message': 'You must be a manager to register a unit'}), 400
		request_json = request.get_json()
		block_id = request_json.get('block_id')
		unit_number = request_json.get('unit_number')
		status_occupied = Status.query.filter_by(status_code=6).first()
		unit_status = status_occupied.status_meaning
		unit_public_id = str(uuid.uuid4())
		unit = Unit(block_id, unit_number, unit_status, unit_public_id)
		db.session.add(unit)
		db.session.commit()
		response_object = {
			'unit_id': unit.unit_id,
			'block_id': unit.block_id,
			'unit_status': unit.unit_status,
			'public_id': unit.public_id
		}

		return jsonify(response_object), 201
	return jsonify({'error': 'Invalid Method'}), 400


#View all units
@app.route('/Units')
def units():
	units = Unit.query.all()
	unitsList = []
	for unit in units:
		units_dict = {
				'block_id': unit.block_id,
				'unit_status': unit.unit_status,
				'public_id': unit.public_id,
				}
		unitsList.append(units_dict)

	return jsonify({'data': unitsList}), 200


#Vacant Units
@app.route('/VacantUnits/<public_id>')
def vacant_unit(public_id):
	block = Block.query.fliter_by(public_id=public_id).first()
	status = Status.query.filter_by(status_code=6).first()
	units = Unit.query.filter_by(block_id=block.block_id, unit_status=status.status_meaning).all()
	units_list = []
	for unit in units:
		unit_dict = {
			'public_id': unit.public_id,
			'unit_status': status.status_meaning,
			'block_id': unit.block_id
		}
		units_list.append(unit_dict)
	return jsonify(units_list), 200


#View a single unit
@app.route('/Unit/<public_id>/')
def unit(public_id):
	unit = Unit.query.filter_by(public_id=public_id).first()
	if not unit:
		return jsonify({'message': 'No such unit.'}), 400
	unit_dict = {
		'block_id': unit.block_id,
		'unit_status': unit.unit_status,
		'public_id': unit.public_id
	}
	return jsonify({'data': unit_dict})


#View a user Unit using user's public_id
@app.route('/TenantUnit/<public_id>/')
def tenant_unit(public_id):
	user = User.query.get(public_id)
	tenant = Tenant.query.filter_by(email=user.email).first()
	lease = Lease.query.filter_by(tenant_id=tenant.tenant_id).first()
	unit = Unit.query.get(lease.unit_id)
	unit_dict = {
		'unit_id': unit.unit_id,
		'block_id': unit.block_id,
		'public_id': unit.public_id
	}
	return jsonify(unit_dict), 200


#Update  Unit details using unit public_id
@app.route('/UpdateUnit/<public_id>/', methods=['POST', 'GET'])
def update_unit(public_id):
	if request.method == 'POST':
		request_json = request.get_json()
		new_status = request_json.get('unit_status')
		unit = Unit.query.filter_by(public_id=public_id).first()
		unit.unit_status = new_status
		db.session.commit()
		response_object = {
			'Message': 'Unit Status has been updated successfully',
			'block_id': unit.block_id,
			'new_status': unit.unit_status
		}
		return jsonify(response_object), 200


	#Delete a Unit
@app.route('/DeleteUnit/<public_id>/', methods=['DELETE'])
def delete_unit(public_id):
		unit = Unit.query.filter_by(public_id).first()
		db.session.delete(unit)
		db.session.commit()
		return jsonify({'message': 'The Unit has been deleted!'}), 200

