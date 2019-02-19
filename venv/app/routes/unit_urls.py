from flask import Flask, session, logging, request, json, jsonify


#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.user import User


@app.route('/InsertHouses', methods =['GET', 'POST'])
def insert_houses():
	#form = HousesForm(request.form)
	if request.method == 'POST':

		request_json = request.get_json()
		Number = request_json.get('Number')
		Price = request_json.get('Price')
		Type = request_json.get('Type')
		user_id = request_json.get('user_id')  
		building_id = request_json.get('building_id')

		house = House(Number, Price, Type, user_id, building_id)
		db.session.add(house)
		db.session.commit()

		return ("Success",200)
	return ("Invalid Method")

#View all houses

@app.route('/houses')
def houses():
	houses = House.query.all()
	housesList = []
	for house in houses:
		houses_dict = {
				'house_number': house.house_number,
				'price': house.price,
				'house_type': house.house_type
				}
		housesList.append(houses_dict)

	return jsonify({'data' :housesList}) 

#View a single house

@app.route('/house/<string:id>/')
def house(id):
	house = House.query.get(id)
	house_dict = {
		'house_number': house.house_number,
		'price': house.price,
		'house_type': house.house_type	
	}
	
	return jsonify({'data': house_dict})
	  

#Update  House details

@app.route('/updatehouse', methods = ['POST', 'GET'])
def update_house():
	if request.method == 'POST':
		request_json = request.get_json()
		house_number = request_json.get('Number')
		new_price = request_json.get('Price')
		new_house_number = request_json.get('new_number')
		new_type = request_json.get('new_type')
		house = House.query.filter_by(house_number = house_number).first()
		if new_price and new_house_number and new_type:
			house.price = new_price
			db.session.flush()
			house.house_type = new_type
			db.session.flush()
			house.house_number = new_house_number
			db.session.commit()
			return ("House number, price and type have been changed!","Success")
		elif new_price and new_house_number:
			house.price = new_price
			db.session.flush()
			house.house_number = new_house_number
			db.session.commit()
			return ("House number and price have been changed!","Success")
		elif new_price and new_type:
			house.price = new_price
			db.session.flush()
			house.house_type = new_type
			db.session.commit()
			return ("House type and price have been changed!","Success")
		elif new_house_number and new_type:
			house.house_type = new_type
			db.session.flush()
			house.house_number = new_house_number
			db.session.commit()
			return ("House number and type have been changed!","Success")
		elif new_house_number:
			house.house_number = new_house_number
			db.session.commit()
			return ("House number has been changed!", "success")
		elif new_type:
			house.house_type = new_type
			db.session.commit()
			return("House type has been changed!","Success")
		elif new_price:
			house.price = new_price
			db.session.commit()
			return("House Price has been changed", "Success")
			
#Delete a House

@app.route('/deletehouse', methods = ['POST', 'GET'])
def delete_house():
	if request.method =='POST':
		request_json = request.get_json()
		house_number = request_json.get('Number')
		house = House.query.filter_by(house_number = house_number).first()
		db.session.delete(house)
		db.session.commit()

		return('The House has been deleted!', 'danger')
	return("Invalid Method")

