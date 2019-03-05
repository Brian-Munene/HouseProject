from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import os
#file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.images import Image
from database.block import Payment
from database.unit import Unit
from database.block import Lease
from database.block import Debt


#Insert payment
@app.route('/InsertPayment', methods=['POST'])
def insert_payment():
    request_json = request.get_json()
    unit_id = request_json.get('unit_id')
    date_paid = request_json.get('date_paid')
    amount_paid = request_json.get('amount_paid')
    if unit_id is None or date_paid is None or amount_paid is None:
        return jsonify({'message': 'You have empty fields.'}), 400
    if not Unit.query.get(unit_id):
        return jsonify({'message': 'No such unit.'}), 422
    if not Unit.query.filter_by(unit_status='Empty'):
        return jsonify({'message': 'That unit is currently empty'}), 422
    payment = Payment(unit_id, amount_paid, date_paid)
    db.session.add(payment)
    db.session.commit()
    # debt = Debt.query.filter_by(debt_id=payment.debt_id)

    response_object = {
        'unit_id': payment.unit_id,
        'amount_paid': payment.amount_paid,
        'date_paid': payment.date_paid
    }
    return jsonify(response_object), 201





