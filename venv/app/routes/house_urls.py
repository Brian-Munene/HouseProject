from flask import Flask, session, logging, request, json, jsonify


#file imports
from routes import app
from routes import db
from database.house import House
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
	
	return json.dumps(house_dict)
	  

#Update  House details

@app.route('/updatehouse', methods = ['POST', 'GET'])
def update_house():
	if request.method == 'POST':
		request_json = request.get_json()
		house_number = request_json.get('Number')
		new_price = request_json.get('Price')
		
		house = House.query.filter_by(house_number = house_number).first()
		house.price = new_price

		db.session.commit()
		return('House Price updated!', 'success')
		

#Delete a House

@app.route('/deletehouse', methods = ['POST', 'GET'])
def delete_house():
	if request.method =='POST':
		request_json = request.get_json()
		house_number = request_json.get('house_number')
		house = House.query.filter_by(house_number = house_number).first()
		db.session.delete(house)
		db.session.commit()

		return('The House has been deleted!', 'danger')

