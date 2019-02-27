from flask import Flask, session, logging, request, json, jsonify
from datetime import datetime
import arrow
# file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.block import ServiceProviders
from database.block import Services


#Insert Service provider
@app.route('/InsertServiceProvider', methods=['POST'])
def insert_provider():
	request_json = request.get_json()
	name = request_json.get('provider_name')
	contact = request_json.get('provider_contact')
	if name is None and contact is None:
		return jsonify({'message': 'Fill all fields'}), 422
	elif ServiceProviders.query.filter_by(provider_contact=contact).first():
		return jsonify({'message': 'Contact is already in use'}), 422
	provider = ServiceProviders(name, contact)
	db.session.add(provider)
	db.session.commit()
	response_object = {
		'provider_id': provider.provider_id,
		'provider_name': provider.provider_name,
		'provider_contact': provider.provider_contact
	}
	return jsonify(response_object), 200


#View Service Providers
@app.route('/ServiceProviders')
def view_providers():
	providers = ServiceProviders.query.all()
	providers_list = []
	for provider in providers:
		provider_dict = {
			'name': provider.provider_name,
			'contact': provider.provider_contact,
			'id': provider.provider_id
		}
		providers_list.append(provider_dict)
	return jsonify(providers_list), 200


#Filter Service providers using complaint_id
@app.route('/ViewComplaintService/<id>/')
def complaint_service(id):
	services = Services.query.filter_by(complaint_id=id).all()
	services_list = []
	total_cost = 0
	for service in services:
		provider = ServiceProviders.query.filter_by(provider_id=service.provider_id).first()
		service_dict = {
			'cost': service.cost,
			'fixed_date': service.fixed_date,
			'provider_name': provider.provider_name
		}
		total_cost = total_cost + service.cost
		services_list.append(service_dict)
	return jsonify({'services': services_list, 'total_cost': str(total_cost)})


