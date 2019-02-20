from flask import Flask, session, logging, request, json, jsonify
from datetime import datetime
import arrow
#file imports
from routes import app
from routes import db
#from database.complaint import Complaint
from database.complaint import Complaint
from database.user import User
from database.block import Block
from database.unit import Unit
#from database.rental import Image


#Create a complaint route
@app.route('/CreateComplaint', methods=['POST'])
def create_complaint():
    request_json = request.get_json()
    message = request_json.get('message')
    due_date = request_json.get('due_date')
    fixed_date = request_json.get('fixed_date')
    unit_id = request_json.get('unit_id')
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
        'unit_id': complaint.unit_id
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

    complaint_dict = {
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date,
            'unit_id': complaint.unit_id
        }
    return jsonify({'data': complaint_dict})


@app.route('/UpdateComplaint', methods=['POST'])
def update_complant():
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


@app.route('/DeleteComplaint/<string:id>/', methods=['DELETE'])
def delete_complaint(id):
    complaint = Complaint.query.get(id)
    db.session.delete(complaint)
    db.session.commit()
    return "Complaint has been deleted!", "Success"


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


#Block Complaints
@app.route('/BlockComplaints/<id>')
def block_complaints(id):
    units = db.session.query(Block).join(Unit).filter_by(block_id=id).all()
    return units





        

