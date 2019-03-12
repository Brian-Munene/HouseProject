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
from database.block import PropertyManager


#Insert payment using user's public_id
@app.route('/InsertPayment/<public_id>', methods=['POST'])
def insert_payment(public_id):
    request_json = request.get_json()
    unit_id = request_json.get('unit_id')
    payment_type = request_json.get('payment_type')
    amount_paid = request_json.get('amount_paid')
    if unit_id is None or payment_type is None or amount_paid is None:
        return jsonify({'message': 'You have null entries'}), 400
    payment_public_id = str(uuid.uuid4())
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'You must be a user to make a payment'}), 400
    tenant = Tenant.query.filter_by(email=user.email).first()
    tenant_lease_verification = Lease.query.filter_by(tenant_id=tenant.tenant_id, unit_id=unit_id).first()
    if not tenant:
        return jsonify({'message': 'Only tenants can make payments.'}), 400
    if not tenant_lease_verification:
        return jsonify({'message': 'You can not make a payment for a unit you do not occupy'}), 400
    if unit_id is None or amount_paid is None:
        return jsonify({'message': 'You have empty fields.'}), 400
    if not Unit.query.get(unit_id):
        return jsonify({'message': 'No such unit.'}), 422
    if not Unit.query.filter_by(unit_status='Empty'):
        return jsonify({'message': 'That unit is currently empty'}), 422
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Active').first()
    debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
    payment = Payment(unit_id, amount_paid, payment_type, debt.debt_id, payment_public_id)
    db.session.add(payment)
    db.session.flush()
    debt.paid_amount = debt.paid_amount + amount_paid
    db.session.flush()
    if debt.paid_amount == debt.bill_amount:
        payment_status = Status.query.filter_by(status_code=8).first()
        fully_paid = payment_status.status_meaning
        debt.debt_status = fully_paid
        db.session.commit()
    elif debt.paid_amount < debt.bill_amount:
        payment_status = Status.query.filter_by(status_code=9).first()
        partially_paid = payment_status.status_meaning
        debt.debt_status = partially_paid
        db.session.commit()
    elif debt.paid_amount > debt.bill_amount:
        payment_status = Status.query.filter_by(status_code=11).first()
        over_paid = payment_status.status_meaning
        debt.debt_status = over_paid
        db.session.commit()
    amount_left = debt.bill_amount - debt.paid_amount
    tenant_name = tenant.first_name + ' ' + tenant.last_name
    transaction_date = payment.date_paid
    statement_public_id = str(uuid.uuid4())
    statement = Statement(tenant.tenant_id, unit_id, tenant_name, payment_type, amount_paid, amount_left, transaction_date, statement_public_id)
    db.session.add(statement)
    db.session.commit()
    response_object = {
        'unit_id': payment.unit_id,
        'amount_paid': payment.amount_paid,
        'date_paid': payment.date_paid,
        'amount_left': amount_left
    }
    return jsonify({'header': {
      'status': 'success',
      'payment_amount': amount_paid,
      'date_paid': payment.date_paid,
      'balance': amount_left,
    },
        'data': response_object}), 201


#View Tenant payments using user's public_id
@app.route('/Payments/<public_id>')
def payments(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    tenant = Tenant.query.filter_by(email=user.email).first()
    if not tenant:
        return jsonify({'message': 'You must be a tenant to view this information'}), 400
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Active').first()
    payments = Payment.query.filter_by(unit_id=lease.unit_id).all()
    payment_list = []
    debts = Debt.query.filter_by(lease_id=lease.lease_id).all()
    if not debts:
        return jsonify({'message': 'Not debts available'}), 400
    debt_list = []
    if not payments:
        return jsonify({'message': 'No payments have been made'}), 400
    total_debit = 0
    for payment in payments:
        payment_dict = {
            'date': payment.date_paid,
            'amount_paid': payment.amount_paid,
            'type': payment.payment_type,
            'public_id': payment.public_id,
            'lease_id': lease.lease_id
        }
        payment_list.append(payment_dict)
        total_debit = total_debit + payment.amount_paid
    debit = {
        'debit': payment_list,
        'total_debit': total_debit
    }
    total_credit = 0
    for debt in debts:
        debt_dict = {
            'date': debt.debt_date,
            'debt_status': debt.debt_status,
            'bill_amount': debt.bill_amount,
            'debt_id': debt.debt_id,
            'lease_id': debt.lease_id
        }
        total_credit = total_credit + debt.bill_amount
        debt_list.append(debt_dict)
    credit = {
        'credit': debt_list,
        'total_credit': total_credit
    }
    response_object = {
        'debits': debit,
        'credits': credit
    }
    return jsonify(response_object), 200





