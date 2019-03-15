from flask import Flask, session, logging, request, json, jsonify
from datetime import datetime
import arrow
import uuid
#file imports
from routes import app
from routes import db
#from database.complaint import Complaint
from database.complaint import Complaint
from database.user import User
from database.block import Block
from database.unit import Unit
from database.block import Property
from database.block import Caretaker
from database.block import ServiceProviders
from database.block import Services
from database.user import User
from database.block import PropertyManager
from database.block import Landlord


#Create a complaint route
@app.route('/CreateComplaint', methods=['POST'])
def create_complaint():
    request_json = request.get_json()
    message = request_json.get('message')
    due_date = request_json.get('due_date')
    fixed_date = request_json.get('fixed_date')
    unit_id = request_json.get('unit_id')
    complaint_public_id = str(uuid.uuid4())
    if message is None or due_date is None or unit_id is None:
        return jsonify({'message', 'Fields should not be null.'}), 422
    if not Unit.query.filter_by(unit_id=unit_id):
        return jsonify({'message': 'Unit does not exist.'}), 400
    complaint = Complaint(message, due_date, fixed_date, unit_id, complaint_public_id)
    db.session.add(complaint)
    db.session.commit()
    response_object = {
        'status': 'Success',
        'date_posted': complaint.date_posted,
        'message': complaint.message,
        'due_date': complaint.due_date,
        'fixed_date': complaint.fixed_date,
        'unit_id': complaint.unit_id,
        'public_id': complaint.public_id
        }
    return jsonify(response_object), 201


@app.route('/ViewComplaints', methods=['GET'])
def view_complaints():
    complaints = Complaint.query.all()
    if not complaints:
        response_object = {
            'message': 'No complaints',
            'status': 'success'
        }
        return jsonify(response_object), 200
    complaintList = []
    for complaint in complaints:
        services = Services.query.filter_by(complaint_id=complaint.complaint_id).all()
        service_list = []
        total_cost = 0
        for service in services:
            service_dict = {
                'service_id': service.service_id,
                'provider_id': service.provider_id,
                'cost': service.cost
            }
            service_list.append(service_dict)
            total_cost = total_cost + service.cost
        service_total_cost = total_cost
        complaint_dict = {
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date,
            'complaint_id': complaint.complaint_id,
            'public_id': complaint.public_id,
            'service_list': service_list,
            'service_total_cost': service_total_cost
        }
        complaintList.append(complaint_dict)
    return jsonify({'data': complaintList})


#View a single complaint using a single complaint's public_id
@app.route('/ViewSingleComplaint/<public_id>')
def view_single_complaint(public_id):
    complaint = Complaint.query.filter_by(public_id=public_id).first()
    if not complaint:
        response_object = {
            'message': 'No record of that complaint.',
            'status': 'failed'
        }
        return jsonify(response_object), 400
    services = Services.query.filter_by(complaint_id=complaint.complaint_id).all()
    service_list = []
    total_cost = 0
    for service in services:
        provider = ServiceProviders.query.filter_by(provider_id=service.provider_id).first()
        service_dict = {
            'service_id': service.service_id,
            'provider_name': provider.provider_name,
            'cost': service.cost
        }
        service_list.append(service_dict)
        total_cost = total_cost + service.cost
    service_total_cost = total_cost
    complaint_dict = {
            'date_posted': complaint.date_posted,
            'public_id': complaint.public_id,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date,
            'unit_id': complaint.unit_id,
            'service_list': service_list,
            'total_service_cost': service_total_cost
        }
    return jsonify({'data': complaint_dict})


# Update Complaint using complaint's public_id
@app.route('/UpdateComplaint/<public_id>', methods=['POST'])
def update_complaint(public_id):
    request_json = request.get_json()
    new_message = request_json.get('new_message')
    new_due_date = request_json.get('new_due_date')
    fixed_date = request_json.get('fixed_date')

    complaint = Complaint.query.filter_by(public_id=public_id).first()

    if new_message and new_due_date:
        complaint.due_date = new_due_date
        db.session.flush()
        complaint.message = new_message
        db.session.commit()
        return 'Complaint message and due date have been updated!', "Success"
    elif new_message:
        complaint.message = new_message
        db.session.commit()
        return 'Complaint message has been updated!', "Success"
    elif new_due_date:
        complaint.due_date = new_due_date
        db.session.commit()
        return "Complaint due date has been changed", "Success"
    elif fixed_date:
        complaint.fixed_date = fixed_date
        db.session.commit()
        return "Complaint has been fixed!", "success"


# Service performed on a complaint using complaint's public_id
@app.route('/ServiceComplaint/<public_id>', methods=['POST'])
def service_complaint(public_id):
    response_json = request.get_json()
    cost = response_json.get('cost')
    provider_id = response_json.get('provider_id')
    service_public_id = str(uuid.uuid4())
    if cost is None:
        return jsonify({'message': 'Fields should not be null'}), 400
    # Insert Service done
    provider = ServiceProviders.query.get(provider_id)
    if not provider:
        return jsonify({'message': 'No such provider'})
    complaint = Complaint.query.filter_by(public_id=public_id).first()
    service = Services(complaint.complaint_id, provider.provider_id, cost, service_public_id)
    db.session.add(service)
    db.session.commit()
    complaint.fixed_date = service.fixed_date
    db.session.commit()
    response_object = {
        'complaint_id': service.complaint_id,
        'provider_id': provider.provider_id,
        'provider_name': provider.provider_name,
        'provider_contact': provider.provider_contact,
        'fixed_date': service.fixed_date,
        'cost': service.cost
    }
    return jsonify(response_object), 200


#Delete a complaint using the complaint's public_id
@app.route('/DeleteComplaint/<public_id>', methods=['DELETE'])
def delete_complaint(public_id):
    complaint = Complaint.query.filter_by(public_id=public_id).first()
    db.session.delete(complaint)
    db.session.commit()
    return "Complaint has been deleted!", "Success"


#Find the complaint of a single unit using unit's public_id
@app.route('/UnitComplaints/<public_id>')
def unit_complaints(public_id):
    unit = Unit.query.filter_by(public_id=public_id).first()
    complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
    complaintList = []
    for complaint in complaints:
        complaint_dict = {
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date,
            'public_id': complaint.public_id
        }
        complaintList.append(complaint_dict)
    return jsonify({'data': complaintList})


#Block Complaints using block's public_id
@app.route('/BlockComplaints/<public_id>')
def block_complaints(public_id):
    # Blocks
    block = Block.query.filter_by(public_id=public_id).first()
    if not block:
        return jsonify({'message': 'No such block.'}), 400
    block_complaints = []
    units = Unit.query.filter_by(block_id=block.block_id).all()
    for unit in units:
        complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
        for complaint in complaints:
            complaint_dict = {
                'unit_id': unit.unit_id,
                'unit_status': unit.unit_status,
                'complaint_id': complaint.complaint_id,
                'date_posted': complaint.date_posted,
                'message': complaint.message,
                'due_date': complaint.due_date,
                'fixed_date': complaint.fixed_date,
                'public_id': complaint.public_id
            }
            # complaint_list.append()
            block_complaints.append(complaint_dict)
            # complaint_list = []

    return jsonify({'data': block_complaints}), 200


# Property manager Complaints using user's public_id
@app.route('/PropertyManagerComplaints/<public_id>')
def property_manager_complaints(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    manager = PropertyManager.query.filter_by(email=user.email).first()
    # fetch Property using property manager id
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if not properties:
        return jsonify({'message': 'No such property'}), 200
    property_list = []
    for property in properties:
        blocks = Block.query.filter_by(property_id=property.property_id).all()
        for block in blocks:
            units = Unit.query.filter_by(block_id=block.block_id).all()
            for unit in units:
                complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
                # complaints_list = []
                for complaint in complaints:
                    complaint_dict = {}
                    if complaint.fixed_date == '0000-00-00':
                        complaint_dict['complaint_id'] = complaint.complaint_id
                        complaint_dict['complaint_public_id'] = complaint.public_id
                        complaint_dict['property_id'] = property.property_id
                        complaint_dict['property_name'] = property.property_name
                        complaint_dict['block_id'] = block.block_id
                        complaint_dict['unit_id'] = unit.unit_id
                        complaint_dict['unit_status'] = unit.unit_status
                        complaint_dict['date_posted'] = complaint.date_posted
                        complaint_dict['message'] = complaint.message
                        complaint_dict['due_date'] = complaint.due_date
                        complaint_dict['fixed_date'] = complaint.fixed_date
                        complaint_dict['status'] = 'Pending'
                    else:
                        complaint_dict['complaint_id'] = complaint.complaint_id
                        complaint_dict['complaint_public_id'] = complaint.public_id
                        complaint_dict['property_id'] = property.property_id
                        complaint_dict['property_name'] = property.property_name
                        complaint_dict['block_id'] = block.block_id
                        complaint_dict['unit_id'] = unit.unit_id
                        complaint_dict['unit_status'] = unit.unit_status
                        complaint_dict['date_posted'] = complaint.date_posted
                        complaint_dict['message'] = complaint.message
                        complaint_dict['due_date'] = complaint.due_date
                        complaint_dict['fixed_date'] = complaint.fixed_date
                        complaint_dict['status'] = 'Fixed'
                    # complaints_list.append()
                    property_list.append(complaint_dict)
    return jsonify(property_list), 200


# Caretaker assigned complaints using user's public_id
@app.route('/CaretakerComplaints/<public_id>')
def caretaker_complaints(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    caretaker = Caretaker.query.filter_by(email=user.email).first()
    if not caretaker:
        return jsonify({'message': 'You are not a caretaker'}), 400
    caretaker_property = Property.query.filter_by(property_id=caretaker.property_id).first()
    property_complaints = []
    blocks = Block.query.filter_by(property_id=caretaker_property.property_id).all()
    if not blocks:
        return jsonify({'message': 'Blocks not available'}), 400
    for block in blocks:
        units = Unit.query.filter_by(block_id=block.block_id).all()
        for unit in units:
            complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
            complaints_list = []
            for complaint in complaints:
                complaint_dict = {
                    'complaint_id': complaint.complaint_id,
                    'complaint_public_id': complaint.public_id,
                    'property_id': caretaker_property.property_id,
                    'block_id': block.block_id,
                    'unit_id': unit.unit_id,
                    'unit_status': unit.unit_status,
                    'date_posted': complaint.date_posted,
                    'message': complaint.message,
                    'due_date': complaint.due_date,
                    'fixed_date': complaint.fixed_date
                }
                # complaints_list.append(complaint_dict)
                property_complaints.append(complaint_dict)
    return jsonify(property_complaints), 200


# Landlord Complaints using user's public_id
@app.route('/LandlordComplaints/<public_id>/')
def landlord_complaints(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    landlord = Landlord.query.filter_by(email=user.email).first()
    # fetch Property using property manager id
    properties = Property.query.filter_by(landlord_id=landlord.landlord_id).all()
    if not properties:
        return jsonify({'message': 'No such property'}), 200
    property_list = []
    for property in properties:
        blocks = Block.query.filter_by(property_id=property.property_id).all()
        block_list = []
        for block in blocks:
            units = Unit.query.filter_by(block_id=block.block_id).all()
            unit_list = []
            block_dict = {
                'block_name': block.block_name,
                # 'unit_list': unit_list
            }
            block_list.append(block_dict)
            for unit in units:
                complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
                complaints_list = []
                unit_dict = {
                    # 'complaint_list': complaints_list
                }
                unit_list.append(unit_dict)
                for complaint in complaints:
                    services = Services.query.filter_by(complaint_id=complaint.complaint_id).all()
                    service_list = []
                    total_cost = 0
                    for service in services:
                        service_dict = {
                            'service_id': service.service_id,
                            'provider_id': service.provider_id,
                            'cost': service.cost
                        }
                        service_list.append(service_dict)
                        total_cost = total_cost + service.cost
                    service_total_cost = total_cost
                    complaint_dict = {}
                    if complaint.fixed_date == '0000-00-00':
                        complaint_dict['complaint_id'] = complaint.complaint_id
                        complaint_dict['complaint_public_id'] = complaint.public_id
                        complaint_dict['property_id'] = property.property_id
                        complaint_dict['property_name'] = property.property_name
                        complaint_dict['block_id'] = block.block_id
                        complaint_dict['unit_id'] = unit.unit_id
                        complaint_dict['unit_status'] = unit.unit_status
                        complaint_dict['date_posted'] = complaint.date_posted
                        complaint_dict['message'] = complaint.message
                        complaint_dict['due_date'] = complaint.due_date
                        complaint_dict['fixed_date'] = complaint.fixed_date
                        complaint_dict['status'] = 'Pending'
                        complaint_dict['services'] = service_list
                        complaint_dict['total_service_cost'] = service_total_cost
                    else:
                        complaint_dict['complaint_id'] = complaint.complaint_id
                        complaint_dict['complaint_public_id'] = complaint.public_id
                        complaint_dict['property_id'] = property.property_id
                        complaint_dict['property_name'] = property.property_name
                        complaint_dict['block_id'] = block.block_id
                        complaint_dict['unit_id'] = unit.unit_id
                        complaint_dict['unit_status'] = unit.unit_status
                        complaint_dict['date_posted'] = complaint.date_posted
                        complaint_dict['message'] = complaint.message
                        complaint_dict['due_date'] = complaint.due_date
                        complaint_dict['fixed_date'] = complaint.fixed_date
                        complaint_dict['status'] = 'Fixed'
                        complaint_dict['services'] = service_list
                        complaint_dict['total_service_cost'] = service_total_cost
                    property_list.append(complaint_dict)
    return jsonify(property_list), 200
        

