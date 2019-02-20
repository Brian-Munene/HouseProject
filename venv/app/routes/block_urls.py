from flask import Flask, session, logging, request, json, jsonify

#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Block
from database.block import Property

#Create a block
@app.route('/InsertBlock', methods=['GET', 'POST'])
def insert_block():
    if request.method == 'POST':
        request_json = request.get_json()
        property_id = request_json.get('property_id')
        block_name = request_json.get('block_name')
        if property_id is None or block_name is None:
            return jsonify({'message': 'Fields cannot be null'}), 400
        elif not Property.query.get(property_id):
            return jsonify({'message': 'property does not exist'}), 400
        block = Block(property_id, block_name)
        db.session.add(block)
        db.session.commit()
        response_object = {
            'message': 'block successfully created',
            'block_name': block.block_name,
            'property_id': block.property_id,
            'block_id': block.block_id
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
                'block_name': block.block_name
            }
            blocksList.append(blocks_dict)
        return jsonify({'data': blocksList})
    else:
        return jsonify({'message': 'No blocks available'}), 200


@app.route('/ViewSpecificBlock/<id>/')
def view_specific_block(id):
    block = Block.query.get(id)
    if block:
        block_dict = {
            'property_id': block.property_id,
            'block_name': block.block_name
        }
        return jsonify({'data': block_dict})
    else:
        return jsonify({'message': 'No such block'}), 400


@app.route('/UpdateBlock/<id>/', methods=['POST', 'GET'])
def update_block(id):
    if request.method == 'POST':
        request_json = request.get_json()
        new_name = request_json.get('new_block_name')
        block = Block.query.get(id)
        block.block_name = new_name
        db.session.commit()
        response_object = {
            'status': 'success',
            "new_name": block.block_name
        }
        return jsonify(response_object), 200
    return jsonify({'message': 'Method not allowed.'}), 405


@app.route('/DeleteBlock/<id>/', methods=['DELETE'])
def delete_block(id):
    block = Block.query.get(id)
    db.session.delete(block)
    db.session.commit()
    return jsonify({'message': 'block has been deleted'}), 200


