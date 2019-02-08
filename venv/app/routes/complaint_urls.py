from flask import Flask, session, logging, request, json, jsonify
#file imports
from routes import app
from routes import db
#from database.complaint import Complaint
from database.rental import Complaint
from database.user import User
from database.house import Building
from database.house import House

#Create a complaint route
@app.route('/CreateComplaint', methods=['POST'])
def create_complaint():
    request_json = request.get_json()
    date_posted = request_json.get('date_posted')
    message = request_json.get('message')
    due_date = request_json.get('due_date')
    fixed_date = request_json.get('fixed_date')
    user_id = request_json.get('user_id')
    house_id = request_json.get('house_id')

    complaint = Complaint(date_posted, message, due_date, fixed_date, user_id, house_id)
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
    complaint_id = request_json.get('id')
    new_message = request_json.get('new_message')
    new_due_date = request_json.get('new_due_date')
    fixed_date = request_json.get('fixed_date')

    complaint = Complaint.query.filter_by(complaint_id = complaint_id).first()

    if new_message and new_due_date:
        complaint.due_date = new_due_date
        db.session.flush()
        complaint.message = new_message
        db.session.commit()
        return('Complaint message and due date have been updated!', "Success")
    elif new_message:
        complaint.message = new_message
        db.session.commit()
        return('Complaint message has been updated!', "Success")
    elif new_due_date:
        complaint.due_date = new_due_date
        db.session.commit()
        return ("Complaint due date has been changed", "Success")
    elif fixed_date:
        complaint.fixed_date = fixed_date
        db.session.commit()
        return ("Complaint has been fixed!", "success")



@app.route('/DeleteComplaint/<string:id>/')
def delete_complaint(id):
    complaint = Complaint.query.get(id)
    db.session.delete(complaint)
    db.session.commit()
    return("Complaint has been deleted!", "Success")

@app.route('/BuildingComplaints', methods = ['POST'])
def building_complaints():
    if request.method == 'POST':
        request_json = request.get_json()
        building_id = request_json.get('building_id')

        #building = Building.query.filter_by(building_id = building_id).first()
        house = House.query.filter_by(building_id = building_id).first()
        house_id = house.house_id
        complaints = Complaint.query.filter_by(house_id = house_id).all()
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



        

