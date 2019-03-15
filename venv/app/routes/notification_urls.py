from flask import Flask, session, logging, request, json, jsonify
import arrow
import uuid

#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.block import Notification
from database.block import Lease
from database.user import User
from database.block import Tenant
from database.block import Status
from database.block import Statement


#Rent is due Notification using user's public_id
@app.route('/TenantNotifications/<public_id>')
def rent_due(public_id):
    user = User.query.filter_by(public_id=public_id, account_status='Active').first()
    if not user:
        return jsonify({'message': 'You should be a user to get notifications'}), 400
    tenant = Tenant.query.filter_by(email=user.email).first()
    tenant_name = tenant.first_name + ' ' + tenant.last_name
    if not tenant:
        return jsonify({'message': 'Only tenant get notifications'}), 400
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Active').first()
    current_date = arrow.utcnow().date()
    if lease:
        statement_list = []
        statements = Statement.query.filter_by(tenant_id=lease.tenant_id, unit_id=lease.unit_id).all()
        for statement in statements:
            statement_dict = {}
            if statement.transaction_type == 'Invoice':
                statement_dict['transaction_date'] = statement.transaction_date
                statement_dict['transaction_type'] = statement.transaction_type
                statement_dict['credit'] = statement.transaction_amount
                statement_list.append(statement_dict)
            else:
                statement_dict['transaction_date'] = statement.transaction_date
                statement_dict['transaction_type'] = statement.transaction_type
                statement_dict['credit'] = statement.transaction_amount
                statement_list.append(statement_dict)
        return jsonify(statement_list), 200
    elif lease.lease_end_date == current_date:
        return jsonify({'message': 'Your lease is expired'}), 200


