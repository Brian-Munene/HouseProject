from datetime import datetime
from routes import db

# Building model
class Building(db.Model):
    
    __tablename__ = 'buildings'

    building_id = db.Column(db.Integer, primary_key = True)
    building_name = db.Column(db.String(35), nullable = False)
    building_number = db.Column(db.Integer, nullable = False, unique = True)
    building_type = db.Column(db.String(35), nullable = False)
    houses = db.relationship('House', backref = 'buildings', lazy = True)
    
    def __init__(self, building_name, building_number, building_type):
        self.name = name
        self.number = number
        self.building_type = building_type

#House Model
class House(db.Model):

	__tablename__ = 'houses'

	house_id = db.Column(db.Integer, primary_key = True)
	house_number = db.Column(db.Integer, nullable = False, unique = True)
	price = db.Column(db.Float(12), nullable = False)
	house_type = db.Column(db.String(20), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
	building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable = True)
	rentals = db.relationship('Rental', backref = 'houses', lazy = True)
	complaints = db.relationship('Complaint', backref = 'houses', lazy = True)

	def __init__(self, house_number, price, house_type, user_id, building_id):
		self.house_number = house_number
		self.price = price
		self.house_type = house_type
		self.user_id = user_id
		self.building_id = building_id
