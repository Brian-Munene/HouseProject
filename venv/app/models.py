from app import db


#Model for the users table
class User(db.Model):
	
	__tablename__ = 'users'

	userId = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75))
	lastname = db.Column(db.String(75))
	username = db.Column(db.String(75))
	password = db.Column(db.String(100))

#House Model
class House(db.Model):

	__tablename__ = 'houses'

	house_id = db.Column(db.Integer, primary_key = True)
	house_number = db.Column(db.Integer)
	price = db.Column(db.Float(12))
	house_type = db.Column(db.String(20)) 

#rental Model
class Rental(db.Model):

	__tablename__ = 'rental'

	rental_id = db.Column(db.Integer, primary_key = True)
	tenant_name = db.Column(db.String(75), unique = True)
	amount_paid = db.Column(db.Float(12))