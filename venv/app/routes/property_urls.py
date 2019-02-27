from flask import Flask, session, logging, request, json, jsonify

#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Property
from database.block import PropertyManager
from database.block import Landlord
from database.block import Block
from database.rental import Rental
from database.block import Tenant
from database.block import Lease
from database.block import Transactions
from database.user import User


# Insert new Property using property user_id
@app.route('/InsertProperty/<id>', methods=['GET', 'POST'])
def insert_property():
    if request.method == 'POST':
        request_json = request.get_json()
        property_name = request_json.get('property_name')
        landlord_email = request_json.get('landlord_email')
        landlord_password = request_json.get('landlord_password')
        landlord_category = request_json.get('landlord_category')
        landlord_first_name = request_json.get('landlord_first_name')
        landlord_last_name = request_json.get('landlord_last_name')
        landlord_phone = request_json.get('landlord_phone')
        block_name = request_json.get('block_name')
        block_units = request_json.get('block_units')
        caretaker_email = request_json.get('caretaker_email')
        caretaker_category = request_json.get('caretaker_category')
        caretaker_first_name = request_json.get('caretaker_first_name')
        caretaker_last_name = request_json.get('caretaker_last_name')
        caretaker_phone = request.json.get('caretaker_phone')
        caretaker_password = request_json.get('caretaker_password')

        user = User.query.get(id).first()
        if not user:
            return jsonify({'message': 'No such user.'}), 422
        manager = PropertyManager.query.filter_by(email=user.email).first()
        if not manager:
            return jsonify({'message': 'You must be a manager to register property.'}), 400
        if property_name is None or landlord_email is None or landlord_password is None or landlord_category is None or landlord_first_name\
                is None or landlord_last_name is None or landlord_phone is None or block_name is None or block_units is None \
                or caretaker_email is None or caretaker_category is None or caretaker_first_name is None or caretaker_last_name is None or caretaker_phone\
                is None or caretaker_password is None:
            response_object = {
                'message': 'Empty fields are not allowed',
                'status': 'Fail'
            }
            return jsonify(response_object), 400
        else:
            landlord = Landlord(landlord_email, landlord_first_name, landlord_last_name, landlord_phone, landlord_category, landlord_password)
            db.session.add(landlord)
            db.session.commit()
            property = Property(property_name, manager.manager_id, landlord.landlord_id)
            db.session.add(property)
            db.session.commit()
            response_object = {
                'status': 'Success',
                'property_name': property.property_name,
                'manager_id': property.manager_id,
                'landlord_id': property.landlord_id
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
            'landlord_id': property.landlord_id
        }
        propertiesList.append(properties_dict)
    return jsonify({'data': propertiesList})


# View a single Property
@app.route('/Property/<id>/')
def view_property(id):
    property = Property.query.get(id)
    property_dict = {
        'property_id': property.property_id,
        'Property_name': property.property_name,
        'manager_id': property.manager_id,
        'landlord_id': property.landlord_id
    }
    return jsonify(property_dict), 200


#Manager Properties using user_id
@app.route('/ManagerProperties/<id>/')
def manager_property(id):
    user = User.query.get(id)
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
            'landlord_id': property.landlord_id
        }
        propertiesList.append(properties_dict)
    return jsonify({'data': propertiesList})


#Landlord Property using property_id
@app.route('/LandlordProperty/<id>/')
def landlord_property(id):
    property = Property.query.get(id)
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
        'landlord_id': landlord_name
    }
    return jsonify(property_dict), 200


#Landlord Properties using user id
@app.route('/LandlordProperties/<id>/')
def landlord_properties(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'No such user.'}), 422
    landlord = Landlord.query.filter_by(email=user.email).first()
    if not landlord:
        return jsonify({'message': 'Only landlords can view this information'}), 422
    properties = Property.query.filter_by(landlord_id=landlord.landlord_id).all()
    if not properties:
        return jsonify({'Error': 'Landlord does not exist.'}), 200
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
            'property_id': property.property_id,
            'Property_name': property.property_name,
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
                'block_id': block.block_id,
                'unit_list': unit_list
            }
            block_list.append(block_dict)
            for unit in units:
                tenant_list = []
                if unit.unit_status == 6:
                    status = 'Empty'
                elif unit.unit_status == 5:
                    status = 'Occupied'
                else:
                    status = 'Undefined'
                unit_dict = {
                    'unit_id': unit.unit_id,
                    'unit_status': status
                }

                unit_list.append(unit_dict)
    return jsonify({'data': properties_list})


# Update Property Details
@app.route('/UpdateProperty/<id>/', methods=['GET', 'POST'])
def update_property(id):
    if request.method == 'POST':
        property = Property.query.get(id)
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


# Delete a Property
@app.route('/DeleteProperty/<id>/', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get(id)
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'The Property has been deleted!'}), 200



