from routes import db
from datetime import datetime

#rental Model
class Rental(db.Model):

	__tablename__ = 'rentals'
	
	rental_id = db.Column(db.Integer, primary_key = True)
	tenant_name = db.Column(db.String(75), unique = True, nullable = False)
	amount_paid = db.Column(db.Float(12), nullable = False)
	paid_at = db.Column(db.DateTime, nullable = False)
	house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
	
	def __init__ (self,tenant_name, amount_paid, paid_at, house_id, user_id):
		self.tenant_name = tenant_name
		self.amount_paid = amount_paid
		self.paid_at = paid_at
		self.house_id = house_id
		self.user_id = user_id
	
	
	
	
#Complaint Model

class Complaint(db.Model):
	__tablename__ = 'complaints'
	date_posted = db.Column(db.DateTime, nullable = False)
	complaint_id = db.Column(db.Integer, primary_key = True)
	message = db.Column(db.Text(75), nullable = False)
	due_date = db.Column(db.DateTime, nullable = True)
	fixed_date = db.Column(db.DateTime, nullable = True)   
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
	house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable = False)
	#Relationship with images table
	images = db.relationship('Image', backref = 'complaints', lazy = True)

	def __init__(self, date_posted, message, due_date, fixed_date, user_id, house_id):
		self.user_id = user_id
		self.date_posted = date_posted
		self.message = message
		self.due_date = due_date
		self.fixed_date = fixed_date
		self.house_id = house_id


#Images Model
class Image(db.Model):
	image_id = db.Column(db.Integer, primary_key = True)
	image_url = db.Column(db.String(75), nullable = False)
	complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable = False)

	def __init__(self, image_id, image_url):
		self.image_url = image_url