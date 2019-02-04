from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db

@app.route('/InsertRentals', methods = ['GET', 'POST'])
def insert_rentals():
	#form = RentalsForm(request.form)
	if request.method =='POST':

		#fetch form data
		tenant = request.form['tenant_user_name']
		amount = request.form['amount_paid']

		rental = Rental(tenant, amount)
		db.session.add(rental)
		db.session.commit()

		flash('Rental details successfully added', 'success')
		return redirect(url_for('index'))

	return render_template('InsertRentals.html')

#Read all rentals

@app.route('/rentals') 	
def rentals():
	return render_template('rentals.html', rentals = Rental.query.all() )

#read a single rental

@app.route('/rental/<string:tenant_name>/') 	
def rental(tenant_name):
	return render_template('rentals.html', rental = Rental.query.filter_by(tenant_name = tenant_name).first())

#Update rental
@app.route('/updaterental', methods = ['GET', 'POST'])
def update_rental():
	if request.method == 'POST':
		tenant_name = request.form['tenant_name']
		new_amount = request.form['new_amount']

		rental = Rental.query.filter_by(tenant_name = tenant_name).first()
		rental.amount_paid = new_amount

		db.session.commit()
		flash('Payment updated!', 'success')
		return redirect(url_for('index'))
	return render_template('updaterental.html')

#Delete rental
@app.route('/deleterental', methods = ['GET', 'POST'])
def delete_rental():
	if request.method == 'POST':
		tenant = request.form['tenant_name']

		rental = Rental.query.filter_by(tenant_name = tenant).first()
		db.session.delete(rental)
		db.session.commit()

		flash('Rental Details deleted!', 'success')
		return redirect(url_for('index'))
	return render_template('deleterental.html')

