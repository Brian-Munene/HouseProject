from flask import Flask, url_for, session, g, logging, request, json, jsonify
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
#file imports
from routes import app
from routes import db
from database.user import User
from database.block import Landlord
from database.unit import Unit


#View all Landlords
@app.route('/ViewLandlords')
def view_landlords():
	landlords = Landlord.query.all()
	landlord_list = []
	for landlord in landlords:
		landlord_dict = {
			'email': landlord.email,
			'first_name': landlord.first_name,
			'last_name': landlord.last_name
		}
		landlord_list.append(landlord_dict)
	return jsonify(landlord_list), 200
