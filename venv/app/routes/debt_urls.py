from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import os
import uuid
#file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.images import Image
from database.block import Payment
from database.unit import Unit
from database.block import Lease
from database.block import Debt
from database.user import User
from database.block import Tenant
from database.block import Status
from database.block import Statement


#View a Tenant's debts using user's public_id
@app.route('/Debts/<public_id>')
def debts(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    tenant = Tenant.query.filter_by(email=user.email).first()
    if not tenant:
        return jsonify({'message': 'YOu must be a tenant to view this information'}), 400
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Active').first()
    debts = Debt.query.filter_by(lease_id=lease.lease_id).all()
    if not debts:
        return jsonify({'message': 'Not debts available'}), 400
    debt_list = []
    total_credit = 0
    for debt in debts:
        debt_dict = {
            'date': debt.debt_date,
            'debt_status': debt.debt_status,
            'bill_amount': debt.bill_amount,
            'debt_id': debt.debt_id
        }
        total_credit = total_credit + debt.bill_amount
        debt_list.append(debt_dict)
    response_object = {
        'credit': debt_list,
        'total_credit': total_credit
    }
    return jsonify(response_object), 200
