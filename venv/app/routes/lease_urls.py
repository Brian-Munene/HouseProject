from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import uuid
import os
#file imports
from routes import app
from routes import db
from database.block import Payment
from database.unit import Unit
from database.block import Lease
from database.block import Debt
from database.user import User
from database.block import Tenant
from database.block import Status
from database.block import Statement
from database.block import Landlord
from database.block import Property
from database.block import Block
from database.unit import Unit
from database.block import PropertyManager
from database.block import PaymentType


#View Leases using property manager user public_id
@app.route('/ManagerLeases/<public_id>')
def lease(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'You must be a user to renew a lease'}), 400
    manager = PropertyManager.query.filter_by(email=user.email).first()
    if not manager:
        return jsonify({'message': 'You should be a manager to renew a lease'}), 400
    properties = Property.query.filter_by(manager_id=manager.manager_id).all()
    if properties:
        #return jsonify({'message': 'No Properties available'}), 400
        property_list = []
        for property in properties:
            blocks = Block.query.filter_by(property_id=property.property_id).all()
            if blocks:
                #lease_dict['block_list'] = 'No lease available for that Block'
                # return jsonify({'message': 'No lease available for that Block'}), 400
                for block in blocks:
                    units = Unit.query.filter_by(block_id=block.block_id).all()
                    if units:
                        # return jsonify({'message': 'Invalid Unit'}), 400
                        # lease_dict['unit_list'] = 'No lease available for that unit'
                        for unit in units:
                            leases = Lease.query.filter_by(unit_id=unit.unit_id).all()
                            if leases:
                                # return jsonify({'message': 'No lease available for that Unit'}), 400
                                #lease_dict['lease_list'] = 'No lease available for that unit'
                                for lease in leases:
                                    lease_dict = {}
                                    tenant = Tenant.query.filter_by(tenant_id=lease.tenant_id).first()
                                    tenant_name = tenant.first_name + ' ' + tenant.last_name
                                    current_date = arrow.utcnow().date()
                                    days_left = (lease.lease_end_date - current_date).days
                                    term = (lease.lease_end_date - lease.lease_begin_date).days
                                    lease_dict['tenant_name'] = tenant_name
                                    lease_dict['tenant_property'] = property.property_name
                                    lease_dict['property_id'] = property.property_id
                                    lease_dict['tenant_block'] = block.block_name
                                    lease_dict['days_left'] = days_left
                                    lease_dict['term'] = term
                                    lease_dict['unit_id'] = unit.unit_id
                                    lease_dict['block_id'] = block.block_id
                                    lease_dict['tenant_unit_name'] = unit.unit_number
                                    lease_dict['tenant_public_id'] = tenant.public_id
                                    lease_dict['lease_status'] = lease.lease_status
                                    lease_dict['lease_public_id'] = lease.public_id
                                    lease_dict['lease_amount'] = lease.lease_amount
                                    lease_dict['service_charges'] = lease.service_charges
                                    lease_dict['lease_begin_date'] = lease.lease_begin_date
                                    lease_dict['lease_end_date'] = lease.lease_end_date
                                    debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
                                    balance = debt.bill_amount - debt.paid_amount
                                    lease_dict['tenant_balance'] = balance
                                    property_list.append(lease_dict)
                    return jsonify(property_list), 200


# Renew a Tenant's lease using tenant's public_id
@app.route('/RenewLease/<public_id>', methods=['GET', 'POST'])
def renew_lease(public_id):
   if request.method == 'POST':
       tenant = Tenant.query.filter_by(public_id=public_id).first()
       tenant_name = tenant.first_name + ' ' + tenant.last_name
       if not tenant:
           return jsonify({'message': 'Invalid tenant'}), 400
       lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Inactive').first()
       if not lease:
           return jsonify({'message': 'You cannot renew your lease while you have an existing active lease.'}), 400
       debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
       balance = debt.bill_amount - debt.paid_amount
       if debt.debt_status == 'Fully Paid' or debt.debt_status == 'Over Paid':
           request_json = request.get_json()
           unit_id = request_json.get('unit_id')
           lease_begin_date = request_json.get('lease_begin_date')
           lease_end_date = request_json.get('lease_end_date')
           lease_amount = request_json.get('lease_amount')
           promises = request_json.get('promises')
           service_charges = request_json.get('service_charges')
           notes = request_json.get('notes')
           lease_public_id = str(uuid.uuid4())
           status_active = Status.query.filter_by(status_code=3).first()
           lease_status = status_active.status_meaning
           payment_interval = request_json.get('payment_interval')
           lease = Lease(tenant.tenant_id, unit_id, lease_begin_date, lease_end_date, lease_amount, promises,
                         service_charges, notes,
                         lease_status,
                         payment_interval, lease_public_id)
           db.session.add(lease)
           db.session.flush()
           total_lease_amount = lease.lease_amount + lease.service_charges
           if debt.debt_status == 'Fully Paid':
               paid_amount = 0
               status = Status.query.filter_by(status_code=10).first()
               new_debt_status = status.status_meaning
               new_debt_public_id = str(uuid.uuid4())
               new_debt_date = lease_begin_date
               new_debt = Debt(total_lease_amount, paid_amount, new_debt_status, new_debt_date, lease.lease_id,
                               new_debt_public_id)
               db.session.add(new_debt)
               db.session.commit()
           elif debt.debt_status == 'Over Paid':
               paid_amount = -1 * balance
               status = Status.query.filter_by(status_code=10).first()
               new_debt_status = status.status_meaning
               new_debt_public_id = str(uuid.uuid4())
               new_debt_date = lease_begin_date
               new_debt = Debt(total_lease_amount, paid_amount, new_debt_status, new_debt_date, lease.lease_id,
                               new_debt_public_id)
               db.session.add(new_debt)
               db.session.commit()
           tenant_name = tenant.first_name + ' ' + tenant.last_name
           transaction_amount = total_lease_amount
           net_amount = total_lease_amount
           statement_public_id = str(uuid.uuid4())
           transaction_type = PaymentType.query.filter_by(type_code='Ty008').first()
           invoice = transaction_type.type_meaning
           statement = Statement(tenant.tenant_id, unit_id, tenant_name, invoice, transaction_amount, net_amount,
                                 lease_begin_date, statement_public_id)
           db.session.add(statement)
           db.session.flush()
           unit = Unit.query.get(unit_id)
           status = Status.query.filter_by(status_code=5).first()
           unit.unit_status = status.status_meaning
           db.session.commit()
           response_object = {
               'unit_id': lease.unit_id,
               'tenant_name': tenant_name,
               'tenant_id': tenant.tenant_id,
               'lease_begin_date': lease.lease_begin_date,
               'lease_amount': lease.lease_amount,
               'lease_end_date': lease.lease_end_date,
               'promises': lease.promises,
               'notes': lease.notes,
               'service_charges': lease.service_charges,
               'lease_status': lease.lease_status,
               'payment_interval': lease.payment_interval,
               'total_lease_amount': str(total_lease_amount)
           }
           return jsonify(response_object), 201
       else:
           return jsonify({'message': 'Settle your debt of ' + str(balance) + ' before renewing your lease.'}), 400
   elif request.method == 'GET':
       tenant = Tenant.query.filter_by(public_id=public_id).first()
       if not tenant:
           return jsonify({'message': 'Invalid tenant'}), 400
       tenant_name = tenant.first_name + ' ' + tenant.last_name
       lease = Lease.query.filter_by(tenant_id=tenant.tenant_id, lease_status='Inactive').first()
       if not lease:
           return jsonify({'message': 'You cannot renew your lease while you have an existing active lease.'}), 400
       response_object = {
           'unit_id': lease.unit_id,
           'tenant_name': tenant_name,
           'tenant_id': tenant.tenant_id,
           'lease_begin_date': lease.lease_begin_date,
           'lease_amount': lease.lease_amount,
           'lease_end_date': lease.lease_end_date,
           'promises': lease.promises,
           'notes': lease.notes,
           'service_charges': lease.service_charges,
           'lease_status': lease.lease_status,
           'payment_interval': lease.payment_interval
       }
       return jsonify(response_object), 200


#Terminate a lease using tenant's public_id
@app.route('/TerminateLease/<public_id>', methods=['PUT'])
def terminate_lease(public_id):
    tenant = Tenant.query.filter_by(public_id=public_id).first()
    new_unit_status = Status.query.filter_by(status_code=6).first()
    if not tenant:
        return jsonify({'message': 'Invalid Tenant.'}), 400
    tenant_name = tenant.first_name + ' ' + tenant.last_name
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id).first()
    if lease.lease_status == 'Inactive' or lease.lease_status == 'Pending':
        return jsonify({'message': 'The lease is already inactive.'}), 400
    debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
    balance = debt.bill_amount - debt.paid_amount
    if debt.debt_status == 'Fully Paid' or debt.debt_status == 'Over Paid':
        status = Status.query.filter_by(status_code=4).first()
        inactivate = status.status_meaning
        lease.lease_status = inactivate
        db.session.flush()
        unit = Unit.query.filter_by(unit_id=lease.unit_id).first()
        unit.unit_status = new_unit_status.status_meaning
        db.session.commit()
        response_object = {
            'tenant_name': tenant_name,
            'lease_begin_date': lease.lease_begin_date,
            'lease_amount': lease.lease_amount,
            'lease_end_date': lease.lease_end_date,
            'promises': lease.promises,
            'notes': lease.notes,
            'balance': balance,
            'lease_status': lease.lease_status
        }
        return jsonify(response_object), 200
    else:
        status = Status.query.filter_by(status_code=13).first()
        pending = status.status_meaning
        lease.lease_status = pending
        db.session.flush()
        unit = Unit.query.filter_by(unit_id=lease.unit_id).first()
        unit.unit_status = new_unit_status.status_meaning
        db.session.commit()
        response_object = {
            'tenant_name': tenant_name,
            'lease_begin_date': lease.lease_begin_date,
            'lease_amount': lease.lease_amount,
            'lease_end_date': lease.lease_end_date,
            'promises': lease.promises,
            'notes': lease.notes,
            'balance': balance,
            'lease_status': lease.lease_status,
        }
        return jsonify(response_object), 200


#Transfer Lease using tenant's public_id
@app.route('/TransferLease/<public_id>', methods=['POST'])
def transfer_lease(public_id):
    tenant = Tenant.query.filter_by(public_id=public_id).first()
    if not tenant:
        return jsonify({'message': 'You are not a tenant'}), 400
    request_json = request.get_json()
    unit_id = request_json.get('unit_id')
    lease_begin_date = request_json.get('lease_begin_date')
    lease_end_date = request_json.get('lease_end_date')
    lease_amount = request_json.get('lease_amount')
    promises = request_json.get('promises')
    service_charges = request_json.get('service_charges')
    notes = request_json.get('notes')
    lease_public_id = str(uuid.uuid4())
    status_active = Status.query.filter_by(status_code=3).first()
    new_lease_status = status_active.status_meaning
    payment_interval = request_json.get('payment_interval')
    if not unit_id or not lease_begin_date or not lease_end_date or not lease_amount or not promises or not service_charges \
            or not notes or not payment_interval:
        return jsonify({'message': 'You have empty fields'}), 400
    lease = Lease.query.filter_by(tenant_id=tenant.tenant_id).all()
    if lease.lease_status == 'Pending':
        debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
        balance = debt.bill_amount - debt.paid_amount
        return jsonify({'message': 'Settle your debt of ' + str(balance) + ' before renewing your lease.'}), 400
    if lease.lease_status == 'Inactive':
        current_date = arrow.utcnow().date()
        days_stayed = (current_date - lease.lease_begin_date).days
        if days_stayed > 14:
            return jsonify({'message': 'You can not transfer a lease after 14 days'}), 400
        deactivate_lease = Status.query.filter_by(status_code=4).first()
        lease.lease_status = deactivate_lease.status_meaning
        db.session.commit()

    '''
        if lease.lease_status == 'Inactive':
            debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
            balance = debt.bill_amount - debt.paid_amount
            if debt.debt_status == 'Fully Paid' or debt.debt_status == 'Over Paid':
                new_lease = Lease(tenant.tenant_id, unit_id, lease_begin_date, lease_end_date, lease_amount, promises,
                              service_charges, notes,
                              new_lease_status,
                              payment_interval, lease_public_id)
                db.session.add(new_lease)
                db.session.flush()
                total_lease_amount = new_lease.lease_amount + new_lease.service_charges
                if debt.debt_status == 'Fully Paid':
                    paid_amount = 0
                    status = Status.query.filter_by(status_code=10).first()
                    new_debt_status = status.status_meaning
                    new_debt_public_id = str(uuid.uuid4())
                    new_debt_date = lease_begin_date
                    new_debt = Debt(total_lease_amount, paid_amount, new_debt_status, new_debt_date, lease.lease_id,
                                    new_debt_public_id)
                    db.session.add(new_debt)
                    db.session.commit()
                elif debt.debt_status == 'Over Paid':
                    paid_amount = -1 * balance
                    status = Status.query.filter_by(status_code=10).first()
                    new_debt_status = status.status_meaning
                    new_debt_public_id = str(uuid.uuid4())
                    new_debt_date = lease_begin_date
                    new_debt = Debt(total_lease_amount, paid_amount, new_debt_status, new_debt_date, lease.lease_id,
                                    new_debt_public_id)
                    db.session.add(new_debt)
                    db.session.commit()
                tenant_name = tenant.first_name + ' ' + tenant.last_name
                transaction_amount = total_lease_amount
                net_amount = total_lease_amount
                statement_public_id = str(uuid.uuid4())
                transaction_type = PaymentType.query.filter_by(type_code='Ty008').first()
                invoice = transaction_type.type_meaning
                new_statement = Statement(tenant.tenant_id, unit_id, tenant_name, invoice, transaction_amount, net_amount,
                                      lease_begin_date, statement_public_id)
                db.session.add(new_statement)
                db.session.flush()
                new_empty_unit = Unit.query.filter_by(unit_id=lease.unit_id).first()
                status_empty = Status.query.filter_by(status_code=6).first()
                new_empty_unit.unit_status = status_empty.status_meaning
                db.session.flush()
                unit = Unit.query.get(unit_id)
                status = Status.query.filter_by(status_code=5).first()
                unit.unit_status = status.status_meaning
                db.session.commit()
                response_object = {
                    'unit_id': new_lease.unit_id,
                    'tenant_name': tenant_name,
                    'tenant_id': tenant.tenant_id,
                    'lease_begin_date': new_lease.lease_begin_date,
                    'lease_amount': new_lease.lease_amount,
                    'lease_end_date': new_lease.lease_end_date,
                    'promises': new_lease.promises,
                    'notes': new_lease.notes,
                    'service_charges': new_lease.service_charges,
                    'lease_status': new_lease.lease_status,
                    'payment_interval': new_lease.payment_interval,
                    'total_lease_amount': str(total_lease_amount)
                }
                return jsonify(response_object), 201
        if lease.lease_status == 'Active':
            current_date = arrow.utcnow().date()
            days_stayed = (current_date - lease.lease_begin_date).days
            if days_stayed > 14:
                return jsonify({'message': 'You can not transfer a lease after 14 days'}), 400
            deactivate_lease = Status.query.filter_by(status_code=4).first()
            lease.lease_status = deactivate_lease.status_meaning
            db.session.commit()
            debt = Debt.query.filter_by(lease_id=lease.lease_id).first()
            balance = debt.bill_amount - debt.paid_amount
            new_lease = Lease(tenant.tenant_id, unit_id, lease_begin_date, lease_end_date, lease_amount, promises,
                          service_charges, notes,
                          new_lease_status,
                          payment_interval, lease_public_id)
            db.session.add(new_lease)
            db.session.flush()
            total_lease_amount = new_lease.lease_amount + new_lease.service_charges
            if debt.debt_status == 'Fully Paid':
                security = debt.bill_amount / 4
                new_paid_amount = debt.paid_amount - security
                status = Status.query.filter_by(status_code=10).first()
                new_debt_status = status.status_meaning
                new_debt_public_id = str(uuid.uuid4())
                new_debt_date = lease_begin_date
                new_debt = Debt(total_lease_amount, new_paid_amount, new_debt_status, new_debt_date, new_lease.lease_id,
                                new_debt_public_id)
                db.session.add(new_debt)
                db.session.commit()
            elif debt.debt_status == 'Over Paid':
                security = debt.bill_amount / 4
                new_paid_amount = debt.paid_amount - security
                status = Status.query.filter_by(status_code=10).first()
                new_debt_status = status.status_meaning
                new_debt_public_id = str(uuid.uuid4())
                new_debt_date = lease_begin_date
                new_debt = Debt(total_lease_amount, new_paid_amount, new_debt_status, new_debt_date, new_lease.lease_id,
                                new_debt_public_id)
                db.session.add(new_debt)
                db.session.commit()
            elif debt.debt_status == 'Not Paid':
                new_paid_amount = 0
                security = debt.bill_amount / 4
                new_debt_amount = debt.bill_amount + security
                status = Status.query.filter_by(status_code=10).first()
                new_debt_status = status.status_meaning
                new_debt_public_id = str(uuid.uuid4())
                new_debt_date = lease_begin_date
                new_debt = Debt(new_debt_amount, new_paid_amount, new_debt_status, new_debt_date, new_lease.lease_id,
                                new_debt_public_id)
                db.session.add(new_debt)
                db.session.commit()
            tenant_name = tenant.first_name + ' ' + tenant.last_name
            transaction_amount = total_lease_amount
            net_amount = total_lease_amount
            statement_public_id = str(uuid.uuid4())
            transaction_type = PaymentType.query.filter_by(type_code='Ty008').first()
            invoice = transaction_type.type_meaning
            new_statement = Statement(tenant.tenant_id, unit_id, tenant_name, invoice, transaction_amount,
                                  net_amount,
                                  lease_begin_date, statement_public_id)
            db.session.add(new_statement)
            db.session.flush()
            new_empty_unit = Unit.query.filter_by(unit_id=lease.unit_id).first()
            status_empty = Status.query.filter_by(status_code=6).first()
            new_empty_unit.unit_status = status_empty.status_meaning
            db.session.flush()
            unit = Unit.query.get(unit_id)
            status = Status.query.filter_by(status_code=5).first()
            unit.unit_status = status.status_meaning
            db.session.commit()
            response_object = {
                'unit_id': new_lease.unit_id,
                'tenant_name': tenant_name,
                'tenant_id': tenant.tenant_id,
                'lease_begin_date': new_lease.lease_begin_date,
                'lease_amount': new_lease.lease_amount,
                'lease_end_date': new_lease.lease_end_date,
                'promises': new_lease.promises,
                'notes': new_lease.notes,
                'service_charges': new_lease.service_charges,
                'lease_status': new_lease.lease_status,
                'payment_interval': new_lease.payment_interval,
                'total_lease_amount': str(total_lease_amount),
                'total_debt_amount': new_debt.bill_amount
            }
            return jsonify(response_object), 201
'''

