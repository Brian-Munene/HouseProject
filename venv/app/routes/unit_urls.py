from flask import Flask, session, logging, request, json, jsonify


#file imports
from routes import app
from routes import db
from database.unit import Unit
from database.user import User


@app.route('/InsertUnit', methods=['GET', 'POST'])
def insert_unit():
	if request.method == 'POST':

		request_json = request.get_json()
		block_id = request_json.get('block_id')
		unit_status = 6

		unit = Unit(block_id, unit_status)
		db.session.add(unit)
		db.session.commit()
		response_object = {
			'block_id': unit.block_id,
			'unit_status': unit.unit_status
		}

		return jsonify(response_object), 201
	return jsonify({'error': 'Invalid Method'})

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

