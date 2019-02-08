from flask import Flask, session, logging, request,json, jsonify
from datetime import datetime
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db
from database.rental import Rental
from database.user import User

@app.route('/InsertRentals', methods = ['GET', 'POST'])
def insert_rentals():
	#form = RentalsForm(request.form)
	if request.method =='POST':

		request_json = request.get_json()
		tenant = request_json.get('tenant_name')
		amount = request_json.get('amount_paid')
		paid_at = request_json.get('paid_at')
		house_id = request_json.get('house_id')
		user_id = request_json.get('user_id')

		rental = Rental(tenant, amount, paid_at, user_id, house_id)
		db.session.add(rental)
		db.session.commit()

		return('Rental details successfully added', 'success')
	return('Invalid Method')

#Read all rentals

@app.route('/rentals') 	
def rentals():
	rentals = Rental.query.all()
	
	rentalsList = []
	for rental in rentals:
		rentals_dict = {
				'tenant name': rental.tenant_name,
				'amount paid': rental.amount_paid,
				'date_paid': rental.paid_at
				}
		rentalsList.append(rentals_dict)
	return jsonify({'data' :rentalsList})



#read a single rental

@app.route('/rental/<string:tenant_name>/') 	
def rental(tenant_name):
	rental = Rental.query.filter_by(tenant_name = tenant_name).first()
	rental_dict = {
		'Tenant Name': rental.tenant_name,
		'Amount Paid': rental.amount_paid,
		'Paid_At': rental.paid_at
	}

	return jsonify(rental_dict)

#Update rental
@app.route('/updaterental', methods = ['GET', 'POST'])
def update_rental():
	if request.method == 'POST':
		request_json = request.get_json()
		tenant_name = request_json.get('tenant_name')
		new_amount = request_json.get('new_amount')
		new_tenant_name = request_json.get('new_tenant_name')

		rental = Rental.query.filter_by(tenant_name = tenant_name).first()
		
		if new_amount and new_tenant_name:
			rental.tenant_name = new_tenant_name
			db.session.flush()
			rental.amount_paid = new_amount
			db.session.commit()
			return('Tenant name and Payment updated!', 'success')
		elif new_amount:
			rental.amount_paid = new_amount
			db.session.commit()
			return('Payment updated!', 'success')
		elif new_tenant_name:
			rental.tenant_name = new_tenant_name
			db.session.commit()
			return("Tenant name Updated!", "success")

#Delete rental
@app.route('/deleterental', methods = ['GET','POST'])
def delete_rental():
	if request.method == 'POST':
		request_json = request.get_json()
		tenant = request_json.get('tenant_name')

		rental = Rental.query.filter_by(tenant_name = tenant).first()
		db.session.delete(rental)
		db.session.commit()

		return('Rental Details deleted!', 'success')
	return ('Invalid Method')
