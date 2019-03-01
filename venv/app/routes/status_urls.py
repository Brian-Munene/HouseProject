from flask import Flask, logging, request, json, jsonify
import uuid

# file imports
from routes import db, app
from database.block import Status


@app.route('/AddStatus', methods=['POST'])
def add_status():
    request_json = request.get_json()
    public_id = str(uuid.uuid4())
    status_code = request_json.get('status_code')
    status_meaning = request_json.get('meaning')
    if Status.query.filter_by(status_code=status_code).first():
        return jsonify({'message': 'The status code already exists.'}), 400
    status = Status(status_code, status_meaning, public_id)
    db.session.add(status)
    db.session.commit()
    response_object = {
        'public_id': status.public_id,
        'status_code': status.status_code,
        'status_meaning': status.status_meaning
    }
    return jsonify(response_object), 201


@app.route('/ViewStatus')
def view_status():
    statuses = Status.query.all()
    status_list = []
    for status in statuses:
        status_dict = {
            'status_code': status.status_code,
            'status_meaning': status.status_meaning
        }
        status_list.append(status_dict)
    return jsonify({status_list}), 200


