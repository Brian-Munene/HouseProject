from flask import Flask, session, logging, request, json, jsonify
#file imports
from routes import app
from routes import db
#from database.complaint import Complaint
from database.rental import Complaint
from database.user import User

#Create a complaint route
@app.route('/CreateComplaint', methods=['POST'])
def create_complaint():
    request_json = request.get_json()
    date_posted = request_json.get('date_posted')
    message = request_json.get('message')
    due_date = request_json.get('due_date')
    fixed_date = request_json.get('fixed_date')
    user_id = request_json.get('user_id')

    complaint = Complaint(date_posted, message, due_date, fixed_date, user_id)
    db.session.add(complaint)
    db.session.commit()
    return("Complaint added", "Success")

@app.route('/ViewComplaints', methods=['GET'])
def view_complaints():
    complaints = Complaint.query.all()
    complaintList = []
    for complaint in complaints:
        complaint_dict ={
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date
        }
        complaintList.append(complaint_dict)
    return jsonify({'data': complaintList})

@app.route('/ViewSingleComplaint/<string:id>/')
def view_single_complaint(id):
    complaint = Complaint.query.get(id)

    complaint_dict ={
            'date_posted': complaint.date_posted,
            'message': complaint.message,
            'due_date': complaint.due_date,
            'fixed_date': complaint.fixed_date
        }
    return jsonify({'data': complaint_dict})

@app.route('/UpdateComplaint', methods=['POST'])
def update_complant():
    request_json = request.get_json()
    id = request_json.get('id')
    new_message = request_json.get('new_message')

    complaint = Complaint.query.get(id)
    complaint.message = new_message
    db.session.commit()
    return('Complaint message has been updated!', "Success")

@app.route('/DeleteComplaint/<string:id>/')
def delete_complaint(id):
    complaint = Complaint.query.get(id)
    db.session.delete(complaint)
    db.session.commit()
    return("Complaint has been deleted!", "Success")