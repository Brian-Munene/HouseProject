from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,json, jsonify
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db
from database.rental import Rental

@app.route('/InsertRentals', methods = ['GET', 'POST'])
def insert_rentals():
	#form = RentalsForm(request.form)
	if request.method =='POST':

		request_json = request.get_json()
		tenant = request_json.get('tenant_user_name')
		amount = request_json.get('amount_paid')

		rental = Rental(tenant, amount)
		db.session.add(rental)
		db.session.commit()

		return('Rental details successfully added', 'success')

#Read all rentals

@app.route('/rentals') 	
def rentals():
	rentals = Rental.query.all()
	
	rentalsList = []
	for rental in rentals:
		rentals_dict = {
				'tenant name': rental.tenant_name,
				'amount paid': rental.amount_paid
				}
		rentalsList.append(rentals_dict)
	return jsonify({'data' :rentalsList})



#read a single rental

@app.route('/rental/<string:tenant_name>/') 	
def rental(tenant_name):
	rental = Rental.query.filter_by(tenant_name = tenant_name).first()
	rental_dict = {
		'Tenant Name': rental.tenant_name,
		'Amount Paid': rental.amount_paid
	}

	return jsonify(rental_dict)

#Update rental
@app.route('/updaterental', methods = ['GET', 'POST'])
def update_rental():
	if request.method == 'POST':
		request_json = request.get_json()
		tenant_name = request_json.get('tenant_name')
		new_amount = request_json.get('new_amount')

		rental = Rental.query.filter_by(tenant_name = tenant_name).first()
		rental.amount_paid = new_amount

		db.session.commit()
		
		return('Payment updated!', 'success')

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
