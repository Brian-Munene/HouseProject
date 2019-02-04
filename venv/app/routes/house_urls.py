from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db


@app.route('/InsertHouses', methods =['GET', 'POST'])
def insert_houses():
	#form = HousesForm(request.form)
	if request.method == 'POST':

		#fetch form data
		number = request.json['Number']
		price = request.json['Price']
		Type = request.json['Type']

		house = House(number, price, Type)
		db.session.add(house)
		db.session.commit()

		return number, price, Type
		#flash('House scuccessfully added', 'success')
		#return redirect(url_for('index'))
		
	#return render_template('InsertHouses.html')

#View all houses

@app.route('/houses')
def houses():
	return render_template('houses.html', houses = House.query.all() )    

#View a single house

@app.route('/house/<string:id>/')
def house(id):
	return render_template('house.html', house = House.query.get(id))  

#Update  House details

@app.route('/updatehouse', methods = ['POST', 'GET'])
def update_house():
	if request.method == 'POST':
		house_number = request.form['house_number']
		new_price = request.form['new_price']
		house = House.query.filter_by(house_number = house_number).first()
		house.price = new_price

		db.session.commit()
		flash('House Price updated!', 'success')
		return redirect(url_for('index'))
	return render_template('updatehouse.html')

#Delete a House

@app.route('/deletehouse', methods = ['POST', 'GET'])
def delete_house():
	if request.method =='POST':
		house_number = request.form['house_number']
		house = House.query.filter_by(house_number = house_number).first()
		db.session.delete(house)
		db.session.commit()

		flash('The House has been deleted!', 'danger')
		return redirect(url_for('index'))
	return render_template('deletehouse.html')

