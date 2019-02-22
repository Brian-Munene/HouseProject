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
# Insert new Property
@app.route('/InsertProperty', methods=['GET', 'POST'])
def insert_property():
    if request.method == 'POST':
        request_json = request.get_json()
        property_name = request_json.get('property_name')
        manager_id = request_json.get('manager_id')
        landlord_id = request_json.get('landlord_id')
        if property_name is None or manager_id is None or landlord_id is None:
            response_object = {
                'message': 'Empty fields are not allowed',
                'status': 'Fail'
            }
            return jsonify(response_object), 400
        else:
            property = Property(property_name, manager_id, landlord_id)
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


#Manaager Properties
@app.route('/ManagerProperties/<id>/')
def manager_property(id):
    properties = Property.query.filter_by(manager_id=id).all()
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


#Landlord Properties
@app.route('/LandlordProperties/<id>/')
def landlord_properties(id):
    properties = Property.query.filter_by(landlord_id=id).all()
    if not properties:
        return jsonify({'Error': 'Landlord does not exist.'}), 200
    properties_list = []
    for property in properties:
        block_list = []
        properties_dict = {
            'property_id': property.property_id,
            'Property_name': property.property_name,
            'manager_id': property.manager_id,
            'landlord_id': property.landlord_id,
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
                rental_list = []
                unit_dict = {
                    'unit_id': unit.unit_id,
                    'unit_status': unit.unit_status,
                    'rental_list': rental_list
                }
                unit_list.append(unit_dict)
                rentals = Rental.query.filter_by(unit_id=unit.unit_id).all()
                for rental in rentals:
                    tenant_list = []
                    rental_dict = {
                        'rental_id': rental.rental_id,
                        'tenant_list': tenant_list
                    }
                    rental_list.append(rental_dict)
                    tenants = Tenant.query.filter_by(tenant_id=rental.tenant_id).all()
                    for tenant in tenants:
                        lease_list = []
                        tenant_dict = {
                            'tenant_first_name': tenant.first_name,
                            'tenant_last_name': tenant.last_name,
                            'lease_list': lease_list
                        }
                        tenant_list.append(tenant_dict)
                        leases = Lease.query.filter_by(lease_id=rental.lease_id).all()
                        for lease in leases:
                            lease_dict = {
                                'lease_begin_date': lease.lease_begin_date,
                                'lease_end_date': lease.lease_end_date,
                                'lease_amount': lease.lease_amount,
                                'service_charges': lease.service_charges,
                                'payment_interval': lease.payment_interval,
                                'lease_status': lease.lease_status
                            }
                            lease_list.append(lease_dict)
                        tenant_list.append(lease_list)
                    rental_list.append(tenant_list)
                unit_list.append(rental_list)
            block_list.append(unit_list)
        properties_list.append(block_list)
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



