from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import os
#file imports
from routes import app
from routes import db
from database.block import Payment
from database.unit import Unit
from database.block import Lease
from database.block import Debt
from database.user import User
from database.block import Tenant
from database.block import Status
from database.block import Statement
from database.block import Landlord
from database.block import Property
from database.block import Block
from database.unit import Unit
from database.block import PropertyManager


#Tenant statement using user's public_id
@app.route('/TenantStatement/<public_id>')
def tenant_statement(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    response_object = {}
    if not user:
        return jsonify({'message': 'You should be a user to access this route'}), 400
    tenant = Tenant.query.filter_by(email=user.email).first()
    if not tenant:
        return jsonify({'message': 'Only tenant can view these statements'}), 400
    tenant_name = tenant.first_name + ' ' + tenant.last_name
    response_object['tenant_name'] = tenant_name
    if not tenant:
        return jsonify({'message': 'Only tenant can view statements'}), 400
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Active').first()
    unit = Unit.query.filter_by(unit_id=lease.unit_id).first()
    response_object['unit_number'] = unit.unit_number
    block = Block.query.filter_by(block_id=unit.block_id).first()
    response_object['block_name'] = block.block_name
    property = Property.query.filter_by(property_id=block.property_id).first()
    response_object['property_name'] = property.property_name
    response_object['property_id'] = property.property_id
    statements = Statement.query.filter_by(tenant_id=tenant.tenant_id).all()
    if not statements:
        return jsonify({'message': 'No Statements'}), 400
    statement_list = []
    total_credit = 0
    total_debit = 0
    for statement in statements:
        statement_dict = {}
        if statement.transaction_type == 'Invoice':
            debit = 0
            credit = statement.net_amount
            total_debit = total_debit + debit
            total_credit = total_credit + credit
            statement_dict['debit'] = debit
            statement_dict['credit'] = credit
        elif not statement.transaction_type == 'Invoice':
            debit = statement.transaction_amount
            total_debit = total_debit + debit
            statement_dict['credit'] = 0
            statement_dict['debit'] = statement.transaction_amount
        statement_dict['transaction_date'] = statement.transaction_date
        statement_dict['tenant_name'] = statement.tenant_name
        statement_dict['transaction_type'] = statement.transaction_type
        statement_list.append(statement_dict)
    balance = total_credit - total_debit
    response_object['statement'] = statement_list
    response_object['total_debit'] = total_debit
    response_object['total_credit'] = total_credit
    response_object['balance'] = balance
    response_object['current_date'] = str(arrow.utcnow())
    return jsonify(response_object), 200


#Landlord statement using user's public_id
@app.route('/LandlordStatement/<public_id>')
def landlord_statement(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'You should be a user to access this route'}), 400
    landlord = Landlord.query.filter_by(email=user.email).first()
    if not landlord:
        return jsonify({'message': 'Only landlord can view this statement'}), 400
    properties = Property.query.filter_by(landlord_id = landlord.landlord_id).all()
    if not properties:
        return jsonify({'message': 'No properties available'}), 400
    property_list = []
    total_debit = 0
    total_credit = 0
    for property in properties:
        block_list = []
        property_dict = {}
        property_dict['property_name'] = property.property_name
        property_dict['property_id'] = property.property_id
        property_dict['block_list'] = block_list
        property_list.append(property_dict)
        blocks = Block.query.filter_by(property_id=property.property_id).all()
        for block in blocks:
            unit_list = []
            block_dict = {}
            block_dict['block_name'] = block.block_name
            block_dict['block_id'] = block.block_id
            block_dict['unit_list'] = unit_list
            block_list.append(block_dict)
            units = Unit.query.filter_by(block_id=block.block_id).all()
            for unit in units:
                statement_list = []
                unit_dict = {}
                unit_dict['unit_number'] = unit.unit_number
                unit_dict['statement_list'] = statement_list
                unit_list.append(unit_dict)
                lease = Lease.query.filter_by(unit_id=unit.unit_id, lease_status='Active').first()
                statements = Statement.query.filter_by(unit_id=unit.unit_id, tenant_id=lease.tenant_id).all()
                for statement in statements:
                    statement_dict = {}
                    if statement.transaction_type == 'Invoice':
                        debit = 0
                        credit = statement.net_amount
                        total_debit = total_debit + debit
                        total_credit = total_credit + credit
                        statement_dict['debit'] = debit
                        statement_dict['credit'] = credit
                    elif not statement.transaction_type == 'Invoice':
                        debit = statement.transaction_amount
                        total_debit = total_debit + debit
                        statement_dict['credit'] = 0
                        statement_dict['debit'] = statement.transaction_amount
                    statement_dict['transaction_date'] = statement.transaction_date
                    statement_dict['transaction_type'] = statement.transaction_type
                    unit_dict['tenant_name'] = statement.tenant_name
                    block_dict['total_credit'] = total_credit
                    block_dict['total_debit'] = total_debit
                    property_dict['total_credit'] = total_credit
                    property_dict['total_debit'] = total_debit
                    statement_list.append(statement_dict)
    return jsonify(property_list), 200


#PropertyManager statement using user's public_id
@app.route('/PropertyManagerStatement/<public_id>')
def property_manager_statement(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'You should be a user to access this route'}), 400
    manager = PropertyManager.query.filter_by(email=user.email).first()
    if not manager:
        return jsonify({'message': 'Only landlord can view this statement'}), 400
    properties = Property.query.filter_by(manager_id = manager.manager_id).all()
    if not properties:
        return jsonify({'message': 'No properties available'}), 400
    property_list = []
    total_debit = 0
    total_credit = 0
    for property in properties:
        block_list = []
        property_dict = {}
        property_dict['property_name'] = property.property_name
        property_dict['block_list'] = block_list
        property_list.append(property_dict)
        blocks = Block.query.filter_by(property_id=property.property_id).all()
        for block in blocks:
            unit_list = []
            block_dict = {}
            block_dict['block_name'] = block.block_name
            block_dict['block_id'] = block.block_id
            block_dict['unit_list'] = unit_list
            block_list.append(block_dict)
            units = Unit.query.filter_by(block_id=block.block_id).all()
            for unit in units:
                statement_list = []
                unit_dict = {}
                unit_dict['unit_number'] = unit.unit_number
                unit_dict['statement_list'] = statement_list
                unit_list.append(unit_dict)
                lease = Lease.query.filter_by(unit_id=unit.unit_id, lease_status='Active').first()
                statements = Statement.query.filter_by(unit_id=unit.unit_id, tenant_id=lease.tenant_id).all()
                for statement in statements:
                    statement_dict = {}
                    if statement.transaction_type == 'Invoice':
                        debit = 0
                        credit = statement.net_amount
                        total_debit = total_debit + debit
                        total_credit = total_credit + credit
                        statement_dict['debit'] = debit
                        statement_dict['credit'] = credit
                    elif not statement.transaction_type == 'Invoice':
                        debit = statement.transaction_amount
                        total_debit = total_debit + debit
                        statement_dict['credit'] = 0
                        statement_dict['debit'] = statement.transaction_amount
                    statement_dict['transaction_date'] = statement.transaction_date
                    statement_dict['transaction_type'] = statement.transaction_type
                    unit_dict['tenant_name'] = statement.tenant_name
                    block_dict['total_credit'] = total_credit
                    block_dict['total_debit'] = total_debit
                    property_dict['total_credit'] = total_credit
                    property_dict['total_debit'] = total_debit
                    statement_list.append(statement_dict)
    return jsonify(property_list), 200


