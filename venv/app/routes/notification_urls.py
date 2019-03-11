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


#Rent is due Notification using user's public_id
@app.route('/RentDue/<public_id>')
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
        notification = Notification.query.filter_by(recipient_id=tenant.tenant_id).first()
        if not notification:
            notification_message = 'Rent is due'
            recipient_id = tenant.tenant_id
            notification_date = lease.lease_begin_date
            notification_type = 'Due Payment'
            public_id = str(uuid.uuid4())
            notification = Notification(notification_message, recipient_id, notification_date, notification_type,
                                        public_id)
            db.session.add(notification)
            db.session.commit()
            response_object = {
                'notification_message': notification.notification_message,
                'notification_date': notification.notification_date,
                'recipient': tenant_name
            }
            return jsonify(response_object), 200
        if lease.lease_begin_date == current_date.date():
            if not notification:
                notification_message = 'Rent is due'
                recipient_id = tenant.tenant_id
                notification_date = lease.lease_begin_date
                notification_type = 'Due Payment'
                public_id = str(uuid.uuid4())
                notification = Notification(notification_message, recipient_id, notification_date, notification_type,
                                            public_id)
                db.session.add(notification)
                db.session.commit()
                response_object = {
                    'notification_message': notification.notification_message,
                    'notification_date': notification.notification_date,
                    'recipient': tenant_name,
                    'notification_type': notification.notification_type
                }
                return jsonify(response_object), 200
        if not current_date == lease.lease_end_date:
            notification = Notification.query.filter_by(teannt_id=tenant.tenant_id,
                                                        notification_type='Due Payment').first()
            first_notification_date = notification.notification_date.shift(days=30).date()
            notification_message = 'Rent is due'
            recipient_id = tenant.tenant_id
            notification_type = 'Due Payment'
            first_notification_public_id = str(uuid.uuid4())
            notification = Notification(notification_message, recipient_id, first_notification_date, notification_type,
                                        first_notification_public_id)
            db.session.add(notification)
            db.session.commit()
            response_object = {
                'notification_message': notification.notification_message,
                'notification_date': notification.notification_date,
                'recipient': tenant_name,
                'notification_type': notification.notification_type
            }
            return jsonify(response_object), 200
            '''
 if not Lease.query.filter_by(lease.lease_begin_date >= current_date, lease.lease_end_date <= current_date):
        status = Status.query.filter_by(status_code=12).first()
        lease.lease_status = status.status_meaning
        return jsonify({'message': 'Your Lease is expired'}), 400
 '''