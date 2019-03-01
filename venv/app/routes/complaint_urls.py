from flask import Flask, session, logging, request, json, jsonify
from datetime import datetime
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
    if message is None or due_date is None or unit_id is None:
        return jsonify({'message', 'Fields should not be null.'}), 422
    if not Unit.query.get(unit_id):
        return jsonify({'message': 'Unit does not exist.'}), 400
    complaint = Complaint(message, due_date, fixed_date, unit_id)
    db.session.add(complaint)
    db.session.commit()
    response_object = {
        'status': 'Success',
        'date_posted': complaint.date_posted,
        'message': complaint.message,
        'due_date': complaint.due_date,
        'fixed_date': complaint.fixed_date,
        'unit_id': complaint.unit_id,
	    'complaint_id': complaint.complaint_id
    }
    return jsonify(response_object), 201


@app.route('/ViewComplaints', methods=['GET'])
def view_complaints():
    complaints = Complaint.query.all()
    if not complaints:
        response_object = {
            'message': 'No complaints',
            'status': 'failed'
        }
        return jsonify(response_object), 401
    complaintList = []
    for complaint in complaints:

        complaint_dict = {
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date,
            'complaint_id': complaint.complaint_id
        }
        complaintList.append(complaint_dict)
    return jsonify({'data': complaintList})


@app.route('/ViewSingleComplaint/<id>/')
def view_single_complaint(id):
    complaint = Complaint.query.get(id)
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
            'unit_id': complaint.unit_id,
            'total_service_cost': service_total_cost
        }
    return jsonify({'data': complaint_dict})


@app.route('/UpdateComplaint', methods=['POST'])
def update_complaint():
    request_json = request.get_json()
    complaint_id = request_json.get('id')
    new_message = request_json.get('new_message')
    new_due_date = request_json.get('new_due_date')
    fixed_date = request_json.get('fixed_date')

    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first()

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


# Service performed on a complaint using complaint_id
@app.route('/ServiceComplaint/<id>/', methods=['POST'])
def service_complaint(id):
    response_json = request.get_json()
    cost = response_json.get('cost')
    provider_id = response_json.get('provider_id')
    if cost is None:
        return jsonify({'message': 'Fields should not be null'}), 400
    # Insert Service done
    provider = ServiceProviders.query.get(provider_id)
    service = Services(id, provider.provider_id, cost)
    db.session.add(service)
    db.session.commit()

    complaint = Complaint.query.filter_by(complaint_id=id).first()
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


#Delete a complaint using the complaint_id
@app.route('/DeleteComplaint/<id>/', methods=['DELETE'])
def delete_complaint(id):
    complaint = Complaint.query.get(id)
    db.session.delete(complaint)
    db.session.commit()
    return "Complaint has been deleted!", "Success"


#Find the complaint of a single unit using unit_id
@app.route('/UnitComplaints/<id>')
def unit_complaints(id):
    complaints = Complaint.query.filter_by(unit_id=id).all()
    complaintList = []
    for complaint in complaints:
        complaint_dict = {
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date
        }
        complaintList.append(complaint_dict)
    return jsonify({'data': complaintList})


#Block Complaints using block_id
@app.route('/BlockComplaints/<id>/')
def block_complaints(id):
    # Blocks
    blocks = Block.query.filter_by(block_id=id).all()
    if not blocks:
        return jsonify({'message': 'No such block.'}), 400
    block_complaints = []
    for block in blocks:
        units = Unit.query.filter_by(block_id=block.block_id).all()
        units_array = []
        for unit in units:
            if unit.unit_status == 6:
                status = 'Empty'
            else:
                status = 'Occupied'
            units_array.append(unit.unit_id)

            for unit in units_array:
                complaints = Complaint.query.filter_by(unit_id=unit).all()
                # complaint_list = []
                for complaint in complaints:
                    complaint_dict = {
                        'unit_id': unit,
                        'unit_status': status,
                        'date_posted': complaint.date_posted,
                        'message': complaint.message,
                        'due_date': complaint.due_date,
                        'fixed_date': complaint.fixed_date
                    }
                    # complaint_list.append()
                    block_complaints.append(complaint_dict)
    return jsonify({'data': block_complaints}), 200


# Property manager Complaints using user_id
@app.route('/PropertyManagerComplaints/<id>/')
def property_manager_complaints(id):
    user = User.query.get(id)
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
                if unit.unit_status == 6:
                    status = 'Vacant'
                else:
                    status = 'Occupied'
                complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
                # complaints_list = []
                for complaint in complaints:
                    complaint_dict = {
                        'complaint_id': complaint.complaint_id,
                        'property_id': property.property_id,
                        'block_id': block.block_id,
                        'unit_id': unit.unit_id,
                        'unit_status': status,
                        'date_posted': complaint.date_posted,
                        'message': complaint.message,
                        'due_date': complaint.due_date,
                        'fixed_date': complaint.fixed_date
                    }
                    # complaints_list.append()
                    property_list.append(complaint_dict)
    return jsonify(property_list), 200


# Caretaker assigned complaints using user_id
@app.route('/CaretakerComplaints/<id>/')
def caretaker_complaints(id):
    user = User.query.get(id)
    caretaker = Caretaker.query.filter_by(email=user.email).first()
    caretaker = Caretaker.query.get(caretaker.caretaker_id)
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
            if unit.unit_status == 6:
                status = 'Vacant'
            else:
                status = 'Occupied'
            complaints = Complaint.query.filter_by(unit_id=unit.unit_id).all()
            complaints_list = []
            for complaint in complaints:
                complaint_dict = {
                    'property_id': caretaker_property.property_id,
                    'block_id': block.block_id,
                    'unit_id': unit.unit_id,
                    'unit_status': status,
                    'date_posted': complaint.date_posted,
                    'message': complaint.message,
                    'due_date': complaint.due_date,
                    'fixed_date': complaint.fixed_date
                }
                complaints_list.append(complaint_dict)
            property_complaints.append(complaints_list)
    return jsonify(property_complaints), 200


# Landlord Complaints using user_id
@app.route('/LandlordComplaints/<id>/')
def landlord_complaints(id):
    user = User.query.get(id)
    landlord = Landlord.query.filter_by(email=user.email).first()
    # fetch Property using property manager id
    properties = Property.query.filter_by(landlord_id=landlord.landlord_id).all()
    if not properties:
        return jsonify({'message': 'No such property'}), 200
    property_list = []
    for property in properties:
        blocks = Block.query.filter_by(property_id=property.property_id).all()
        block_list = []
        property_dict = {
            'property_name': property.property_name,
            # 'block_list': block_list
        }
        property_list.append(property_dict)
        for block in blocks:
            units = Unit.query.filter_by(block_id=block.block_id).all()
            unit_list = []
            block_dict = {
                'block_name': block.block_name,
                # 'unit_list': unit_list
            }
            block_list.append(block_dict)
            for unit in units:
                if unit.unit_status == 6:
                    status = 'Vacant'
                elif unit.unit_status == 5:
                    status = 'Occupied'
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
                    complaint_dict = {
                        'complaint_id': complaint.complaint_id,
                        'property_name': property.property_name,
                        'block_id': block.block_id,
                        'unit_id': unit.unit_id,
                        'unit_status': status,
                        'date_posted': complaint.date_posted,
                        'message': complaint.message,
                        'due_date': complaint.due_date,
                        'fixed_date': complaint.fixed_date,
                        'total_service_cost': service_total_cost
                    }

                    property_list.append(complaint_dict)
    return jsonify(property_list), 200
        

