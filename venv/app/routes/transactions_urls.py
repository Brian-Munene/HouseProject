from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import os
#file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.images import Image
from database.block import Transactions
from database.unit import Unit


#Insert transaction
@app.route('/InsertTransaction', methods=['POST'])
def insert_transaction():
    request_json = request.get_json()
    unit_id = request_json.get('unit_id')
    date_paid = request_json.get('date_paid')
    amount_paid = request_json.get('amount_paid')
    if unit_id is None or date_paid is None or amount_paid is None:
        return jsonify({'message': 'YOu have empty fields.'}), 400
    if not Unit.query.get(unit_id):
        return jsonify({'message': 'No such unit.'}), 422
    if not Unit.query.filter_by(unit_status=6):
        return jsonify({'message': 'That unit is currently empty'}), 422
    transaction = Transactions(unit_id, amount_paid, date_paid)
    db.session.add(transaction)
    db.session.commit()
    response_object = {
        'unit_id': transaction.unit_id,
        'amount_paid': transaction.amount_paid,
        'date_paid': transaction.date_paid
    }
    return jsonify(response_object), 201





