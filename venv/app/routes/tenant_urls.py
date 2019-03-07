from flask import Flask, url_for, session, g, logging, request, json, jsonify
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.block import Landlord
from database.block import PropertyManager
from database.block import Tenant
from database.unit import Unit
from database.block import Lease
from database.block import Payment


@app.route('/ViewTenants')
def view_tenants():
    tenants = Tenant.query.all()
    tenant_list = []
    for tenant in tenants:
        name = tenant.first_name + ' ' + tenant.last_name
        tenant_dict = {
            'name': name,
            'public_id': tenant.public_id,
            'tenant_id': tenant.tenant_id
        }
        tenant_list.append(tenant_dict)
    return jsonify({'data': tenant_list}), 200


# View single tenant using user's public_id
@app.route('/ViewSingleTenant<public_id>')
def single_tenant(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    tenant = Tenant.query.filter_by(email=user.email).first()
    if not tenant:
        return jsonify({'message': 'You can not view the tenant details'}), 400
    tenant_dict = {
        'first_name': tenant.first_name,
        'last_name': tenant.last_name,
        'public_id': tenant.public_id,
        'tenant_id': tenant.tenant_id
    }
    return jsonify({'data': tenant_dict}), 200

