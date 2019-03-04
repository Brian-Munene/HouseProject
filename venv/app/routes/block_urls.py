from flask import Flask, session, logging, request, json, jsonify
import uuid
#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Block
from database.block import Property


#Create a block using property's public_id
@app.route('/InsertBlock/<public_id>', methods=['GET', 'POST'])
def insert_block(public_id):
    if request.method == 'POST':
        request_json = request.get_json()
        block_name = request_json.get('block_name')
        number_of_units = request_json.get('units')
        property = Property.query.filter_by(public_id=public_id).first()
        block_public_id = str(uuid.uuid4())
        if block_name is None:
            return jsonify({'message': 'Fields cannot be null'}), 400
        elif not property:
            return jsonify({'message': 'property does not exist'}), 400
        block = Block(property.property_id, block_name, number_of_units, block_public_id)
        db.session.add(block)
        db.session.commit()
        response_object = {
            'status': 'block successfully created',
            'block_name': block.block_name,
            'public_id': block.public_id,
            'property_id': block.property_id,
            'block_id': block.block_id,
            'units': block.number_of_units
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
                'public_id':block.public_id
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
