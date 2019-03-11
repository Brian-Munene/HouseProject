from flask import Flask, session, logging, request, json, jsonify
import uuid
#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Property
from database.block import PropertyManager
from database.block import Landlord
from database.block import Block
from database.block import Tenant
from database.block import Lease
from database.block import Payment
from database.block import Caretaker
from database.user import User


# Insert new Property using user's public_id
@app.route('/InsertProperty/<public_id>', methods=['GET', 'POST'])
def insert_property(public_id):
    if request.method == 'POST':
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'No such user.'}), 422
        manager = PropertyManager.query.filter_by(email=user.email).first()
        if not manager:
            return jsonify({'message': 'Only managers can view this information'}), 422
        request_json = request.get_json()
        property_name = request_json.get('property_name')
        landlord_id = request_json.get('landlord_id')
        property_public_id = str(uuid.uuid4())
        if property_name is None or landlord_id is None:
            response_object = {
                'message': 'Empty fields are not allowed',
                'status': 'Fail'
            }
            return jsonify(response_object), 400
        if not Landlord.query.get(landlord_id):
            return jsonify({'message': 'This user is not a landlord.'}), 400
        else:
            property = Property(property_name, manager.manager_id, landlord_id, property_public_id)
            db.session.add(property)
            db.session.commit()
            response_object = {
                'status': 'Success',
                'property_name': property.property_name,
                'manager_id': property.manager_id,
                'landlord_id': property.landlord_id,
                'public_id': property.public_id
            }
            return jsonify(response_object), 201
    else:
        return jsonify({'message': 'Method not allowed'}), 405


# View All property
@app.route('/Properties')
def view_properties():
    properties = Property.query.all()
    propertiesList = []
    for property in properties:
        properties_dict = {
            'property_id': property.property_id,
            'Property_name': property.property_name,
            'manager_id': property.manager_id,
            'landlord_id': property.landlord_id,
            'public_id': property.public_id
        }
        propertiesList.append(properties_dict)
    return jsonify({'data': propertiesList})


# View a single Property using property's public_id
@app.route('/Property/<public_id>')
def view_property(public_id):
    property = Property.query.filter_by(public_id=public_id).first()
    landlord = Landlord.query.filter_by(landlord_id=property.landlord_id).first()
    manager = PropertyManager.query.filter_by(manager_id=property.manager_id).first()
    caretakers = Caretaker.query.filter_by(property_id=property.property_id).all()
    blocks = Block.query.filter_by(property_id=property.property_id).all()
    landlord_name = landlord.first_name + ' ' + landlord.last_name
    manager_name = manager.first_name + ' ' + manager.last_name
    caretakers_list = []
    blocks_list = []
    property_dict = {
        'property_id': property.property_id,
        'Property_name': property.property_name,
        'manager': manager_name,
        'caretaker': caretakers_list,
        'block_name': blocks_list,
        'landlord': landlord_name,
        'public_id': property.public_id
    }
    for block in blocks:
        block_dict = {
            'block_units': block.number_of_units,
            'block_name': block.block_name,
            'block_public_id': block.public_id,
        }
        blocks_list.append(block_dict)
    for caretaker in caretakers:
        name = caretaker.first_name + ' ' + caretaker.last_name
        caretaker_dict = {
            'caretaker_name': name
        }
        caretakers_list.append(caretaker_dict)
    return jsonify(property_dict), 200


#Manager Properties using user's public_id
@app.route('/ManagerProperties/<public_id>/')
def manager_property(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    manager = PropertyManager.query.filter_by(email=user.email).first()
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if not properties:
        return jsonify({'Error': 'Manager does not exist.'}), 200
    propertiesList = []
    for property in properties:
        properties_dict = {
            'property_id': property.property_id,
            'Property_name': property.property_name,
            'manager_id': property.manager_id,
            'landlord_id': property.landlord_id,
            'public_id': property.public_id
        }
        propertiesList.append(properties_dict)
    return jsonify({'data': propertiesList})


#Landlord Property using property's public_id
@app.route('/LandlordProperty/<public_id>')
def landlord_property(public_id):
    property = Property.query.filter_by(public_id=public_id).first()
    if not property:
        return jsonify({'message': 'No such Property.'}), 400
    manager = PropertyManager.query.get(property.manager_id)
    manager_name = manager.first_name + ' ' + manager.last_name
    if not manager:
        manager_name = 'No Manager'
    landlord = Landlord.query.get(property.landlord_id)
    landlord_name = landlord.first_name + ' ' + landlord.last_name
    if not landlord:
        landlord_name = 'No Landlord'
    property_dict = {
        'property_name': property.property_name,
        'manager_id': manager_name,
        'landlord_id': landlord_name,
        'public_id': property.public_id
    }
    return jsonify(property_dict), 200


#Landlord Properties using user's public_id
@app.route('/LandlordProperties/<public_id>')
def landlord_properties(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No such user.'}), 422
    landlord = Landlord.query.filter_by(email=user.email).first()
    if not landlord:
        return jsonify({'message': 'Only landlords can view this information'}), 422
    properties = Property.query.filter_by(landlord_id=landlord.landlord_id).all()
    if not properties:
        return jsonify({'Error': 'Property does not exist.'}), 200
    properties_list = []
    for property in properties:
        block_list = []
        manager = PropertyManager.query.get(property.manager_id)
        manager_name = manager.first_name + ' ' + manager.last_name
        if not manager:
            manager_name = 'No Manager'
        landlord = Landlord.query.get(property.landlord_id)
        landlord_name = landlord.first_name + ' ' + landlord.last_name
        if not landlord:
            landlord_name = 'No Landlord'
        properties_dict = {
            'property_public_id': property.public_id,
            'Property_name': property.property_name,
            'Property_id': property.property_id,
            'manager_id': manager_name,
            'landlord_id': landlord_name,
            'block_list': block_list
        }
        properties_list.append(properties_dict)
        blocks = Block.query.filter_by(property_id=property.property_id)
        for block in blocks:
            units = Unit.query.filter_by(block_id=block.block_id).all()
            unit_list = []
            block_dict = {
                'block_name': block.block_name,
                'block_public_id': block.public_id,
                'unit_list': unit_list
            }
            block_list.append(block_dict)
            for unit in units:
                tenant_list = []
                unit_dict = {
                    'unit_public_id': unit.public_id,
                    'unit_status': unit.unit_status
                }

                unit_list.append(unit_dict)
    return jsonify({'data': properties_list})


# Update Property Details
@app.route('/UpdateProperty/<public_id>', methods=['GET', 'POST'])
def update_property(public_id):
    if request.method == 'POST':
        property = Property.query.filter_by(public_id=public_id).first()
        request_json = request.get_json()
        new_name = request_json.get('property_name')
        manager_id = request_json.get('manager_id')
        landlord_id = request_json.get('landlord_id')
        if not PropertyManager.query.get(manager_id):
            return jsonify({'Error': 'Manager does not exist.'}), 200
        elif not Landlord.query.get(landlord_id):
            return jsonify({'Error': 'Landlord does not exist.'}), 200
        else:
            if new_name and manager_id and landlord_id:
                property.property_name = new_name
                db.session.flush()
                property.manager_id = manager_id
                db.session.flush()
                property.landlord_id = landlord_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif new_name and manager_id:
                property.property_name = new_name
                db.session.flush()
                property.manager_id = manager_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif manager_id and landlord_id:
                property.manager_id = manager_id
                db.session.flush()
                property.landlord_id = landlord_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif new_name and landlord_id:
                property.property_name = new_name
                db.session.flush()
                property.landlord_id = landlord_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif new_name:
                property.property_name = new_name
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif manager_id:
                property.manager_id = manager_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            elif landlord_id:
                property.landlord_id = landlord_id
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'property_name': property.property_name,
                    'manager_id': property.manager_id,
                    'landlord_id': property.landlord_id
                }
                return jsonify(response_object), 200
            else:
                return jsonify({'message': 'No updates made'}), 400
    else:
        return jsonify({'message': 'Method not Allowed'}), 405


# Delete a Property using the property's public_id
@app.route('/DeleteProperty/<public_id>', methods=['DELETE'])
def delete_property(public_id):
    property = Property.query.filter_by(public_id=public_id).first()
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'The Property has been deleted!'}), 200



