from flask import Flask, session, logging, request, json, jsonify
import uuid
import arrow
#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Block
from database.block import Property
from database.block import Tenant
from database.block import Lease
from database.block import Status


#Create a block using property's public_id
@app.route('/InsertBlock/<public_id>', methods=['GET', 'POST'])
def insert_block(public_id):
    if request.method == 'POST':
        request_json = request.get_json()
        block_name = request_json.get('block_name')
        number_of_units = request_json.get('units')
        property = Property.query.filter_by(public_id=public_id).first()
        block_public_id = str(uuid.uuid4())
        if not block_name:
            return jsonify({'message': 'Fields cannot be null'}), 400
        elif not property:
            return jsonify({'message': 'property does not exist'}), 400
        block = Block(property.property_id, block_name, number_of_units, block_public_id)
        db.session.add(block)
        db.session.commit()
        unit_list = []
        units_number = int(number_of_units) + 1
        for i in range(1, units_number):
            unit_number = property.property_name + '-' + block.block_name + '-U' + str(i)
            status_occupied = Status.query.filter_by(status_code=6).first()
            unit_status = status_occupied.status_meaning
            unit_public_id = str(uuid.uuid4())
            unit = Unit(block.block_id, unit_number, unit_status, unit_public_id)
            db.session.add(unit)
            db.session.commit()
            unit_dict = {
                'unit_id': unit.unit_id,
                'unit_public_id': unit.public_id,
                'unit_number': unit.unit_number
            }
            unit_list.append(unit_dict)

        response_object = {
            'status': 'block successfully created',
            'block_name': block.block_name,
            'public_id': block.public_id,
            'property_id': block.property_id,
            'block_id': block.block_id,
            'number_of_units': block.number_of_units,
            'units': unit_list
        }
        return jsonify(response_object), 201


@app.route('/ViewBlocks')
def view_blocks():
    blocks = Block.query.all()
    if blocks:
        blocksList = []
        for block in blocks:
            blocks_dict = {
                'property_id': block.property_id,
                'block_name': block.block_name,
                'public_id': block.public_id
            }
            blocksList.append(blocks_dict)
        return jsonify({'data': blocksList})
    else:
        return jsonify({'message': 'No blocks available'}), 200


@app.route('/ViewSpecificBlock/<public_id>/')
def view_specific_block(public_id):
    block = Block.query.filter_by(public_id=public_id).first()
    if block:
        block_dict = {
            'property_id': block.property_id,
            'public_id': block.public_id,
            'block_name': block.block_name
        }
        return jsonify({'data': block_dict})
    else:
        return jsonify({'message': 'No such block'}), 400


@app.route('/UpdateBlock/<public_id>/', methods=['POST', 'GET'])
def update_block(public_id):
    if request.method == 'POST':
        request_json = request.get_json()
        new_name = request_json.get('new_block_name')
        block = Block.query.filter_by(public_id=public_id).first()
        block.block_name = new_name
        db.session.commit()
        response_object = {
            'status': 'success',
            'new_name': block.block_name,
            'public_id': block.public_id
        }
        return jsonify(response_object), 200
    return jsonify({'message': 'Method not allowed.'}), 405


@app.route('/DeleteBlock/<public_id>', methods=['DELETE'])
def delete_block(public_id):
    block = Block.query.filter_by(public_id=public_id).first()
    db.session.delete(block)
    db.session.commit()
    return jsonify({'message': 'block has been deleted'}), 200


#View Property blocks using property public_id
@app.route('/PropertyBlocks/<public_id>')
def property_blocks(public_id):
    property = Property.query.filter_by(public_id=public_id).first()
    if not property:
        return({'message': 'No such property'}), 400
    blocks = Block.query.filter_by(property_id=property.property_id).all()
    blocks_list = []
    for block in blocks:
        block_dict = {
            'block_name': block.block_name,
            'public_id': block.public_id,
            'units': block.number_of_units,
            'block_id': block.block_id
        }
        blocks_list.append(block_dict)
    return jsonify(blocks_list), 200


#View Block units using block's public_id
@app.route('/BlockUnits/<public_id>')
def block_unit(public_id):
    block = Block.query.filter_by(public_id=public_id).first()
    property = Property.query.get(block.property_id)
    units = Unit.query.filter_by(block_id=block.block_id).all()
    units_list = []
    block_dict = {
        'block_name': block.block_name,
        'property_name': property.property_name,
        'unit_list': units_list
    }
    for unit in units:
        tenant_name = []
        unit_dict = {
            'unit_id': unit.unit_id,
            'unit_public_id': unit.public_id,
            'unit_status': unit.unit_status,
            'tenant_name': tenant_name,
            'unit_number': unit.unit_number
        }
        units_list.append(unit_dict)
        if unit.unit_status == 'Occupied':
            lease = Lease.query.filter_by(lease_status='Active', unit_id=unit.unit_id).first()
            tenant = Tenant.query.filter_by(tenant_id=lease.tenant_id).first()
            name = tenant.first_name + ' ' + tenant.last_name
            tenant_name.append(name)
    return jsonify({'data': block_dict}), 200


