from datetime import datetime
from routes import db

#House Model
class House(db.Model):

	__tablename__ = 'houses'

	id = db.Column(db.Integer, primary_key = True)
	house_number = db.Column(db.Integer)
	price = db.Column(db.Float(12))
	house_type = db.Column(db.String(20))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
	building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable = False)
	rentals = db.relationship('Rental', backref = 'houses', lazy = True)

	def __init__(self, house_number, price, house_type):
		self.house_number = house_number
		self.price = price
		self.house_type = house_type
