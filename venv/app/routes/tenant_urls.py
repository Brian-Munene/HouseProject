from flask import Flask, url_for, session, g, logging, request, json, jsonify
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.block import Landlord
from database.block import PropertyManager
from database.block import Property
from database.block import Tenant
from database.unit import Unit
from database.block import Block
from database.block import Lease
from database.block import Payment
from database.block import Statement


@app.route('/ViewTenants')
def view_tenants():
    tenants = Tenant.query.all()
    tenant_list = []
    for tenant in tenants:
        name = tenant.first_name + ' ' + tenant.last_name
        tenant_dict = {
            'name': name,
            'public_id': tenant.public_id,
            'tenant_id': tenant.tenant_id
        }
        tenant_list.append(tenant_dict)
    return jsonify({'data': tenant_list}), 200


# View single tenant using user's public_id
@app.route('/ViewSingleTenant<public_id>')
def single_tenant(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    tenant = Tenant.query.filter_by(email=user.email).first()
    if not tenant:
        return jsonify({'message': 'You can not view the tenant details'}), 400
    tenant_dict = {
        'first_name': tenant.first_name,
        'last_name': tenant.last_name,
        'public_id': tenant.public_id,
        'tenant_id': tenant.tenant_id
    }
    return jsonify({'data': tenant_dict}), 200


#View Property manager tenants using manager's user_public_id
@app.route('/PropertyManagerTenants/<public_id>')
def view_manager_tenants(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Invalid User'}), 400
    manager = PropertyManager.query.filter_by(email=user.email).first()
    if not manager:
        return jsonify({'message': 'Only property managers can view Tenants'}), 400
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if properties:
        property_list = []
        for property in properties:

            blocks = Block.query.filter_by(property_id=property.property_id).all()
            if blocks:
                for block in blocks:
                    units = Unit.query.filter_by(block_id=block.block_id).all()
                    if units:
                        for unit in units:
                            leases = Lease.query.filter_by(unit_id=unit.unit_id).all()
                            if leases:
                                for lease in leases:
                                    tenant_dict = {}
                                    tenant = Tenant.query.filter_by(tenant_id=lease.tenant_id).first()
                                    tenant_name = tenant.first_name + ' ' + tenant.last_name
                                    tenant_dict['lease_status'] = lease.lease_status
                                    tenant_dict['lease_amount'] = str(lease.lease_amount + lease.service_charges)
                                    tenant_dict['tenant_name'] = tenant_name
                                    tenant_dict['unit_id'] = unit.unit_id
                                    tenant_dict['property_name'] = property.property_name
                                    tenant_dict['tenant_public_id'] = tenant.public_id
                                    tenant_dict['unit_number'] = unit.unit_number
                                    property_list.append(tenant_dict)
        return jsonify(property_list), 200


#Update Landlord_information using tenant's public_id
@app.route('/UpdateTenant/<public_id>', methods=['POST', 'GET'])
def update_tenant(public_id):
    if request.method == 'GET':
        tenant = Tenant.query.filter_by(public_id=public_id).first()
        if not tenant:
            return jsonify({'message': 'Invalid tenant'}), 400
        tenant_dict = {
            'first_name': tenant.first_name,
            'last_name': tenant.last_name,
            'email': tenant.email,
            'phone': tenant.phone
        }
        return jsonify(tenant_dict), 200
    if request.method == 'POST':
        tenant = Tenant.query.filter_by(public_id=public_id).first()
        if not tenant:
            return jsonify({'message': 'Not a tenant'}), 400
        old_first_name = tenant.first_name
        old_last_name = tenant.last_name
        old_email = tenant.email
        old_phone = tenant.phone
        request_json = request.get_json()
        first_name = request_json.get('first_name')
        last_name = request_json.get('last_name')
        email = request_json.get('email')
        phone = request_json.get('phone')
        response_object = {}
        if not first_name == old_first_name:
            tenant.first_name = first_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_first_name'] = old_first_name
            response_object['new_first_name'] = first_name
        if not last_name == old_last_name:
            tenant.last_name = last_name
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_last_name'] = old_last_name
            response_object['new_last_name'] = last_name
        if not email == old_email:
            user = User.query.filter_by(email=old_email).first()
            user.email = email
            db.session.flush()
            tenant.email = email
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_email'] = old_email
            response_object['new_email'] = email
        if not phone == old_phone:
            tenant.phone = phone
            db.session.commit()
            response_object['status'] = 'Change Successful'
            response_object['old_phone'] = old_phone
            response_object['new_phone'] = phone
        return jsonify(response_object), 200


