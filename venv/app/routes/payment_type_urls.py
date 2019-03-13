from flask import Flask, logging, request, json, jsonify
import uuid

# file imports
from routes import db, app
from database.block import PaymentType


@app.route('/InsertType', methods=['POST'])
def insert_type():
    request_json = request.get_json()
    public_id = str(uuid.uuid4())
    type_code = request_json.get('type_code')
    type_meaning = request_json.get('type_meaning')
    if PaymentType.query.filter_by(type_code=type_code).first():
        return jsonify({'message': 'Code exists'}), 400
    elif PaymentType.query.filter_by(type_meaning=type_meaning).first():
        return jsonify({'message': 'Payment type already registered'}), 400
    type = PaymentType(public_id, type_code, type_meaning)
    db.session.add(type)
    db.session.commit()
    response_object = {
        'type': type.type_meaning,
        'type_code': type.type_code
    }
    return jsonify(response_object), 201


@app.route('/ViewTypes')
def payment_types():
    types = PaymentType.query.all()
    types_list = []
    for type in types:
        type_dict = {
            'type_code': type.type_code,
            'type_meaning': type.type_meaning
        }
        types_list.append(type_dict)
    return jsonify({'data': types_list}), 200
