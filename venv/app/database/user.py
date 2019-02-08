from passlib.apps import custom_app_context as pwd_context
#file imports
from routes import db


#User model
class User(db.Model):

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)
	
	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)
	
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75), nullable = False)
	lastname = db.Column(db.String(75), nullable = False)
	username = db.Column(db.String(75), unique = True, nullable = False)
	password_hash = db.Column(db.String(128), nullable = False)
	category = db.Column(db.String(30), nullable = False)
	houses = db.relationship('House', backref = 'users', lazy = True)
	rental = db.relationship('Rental', backref = 'users', lazy = True)
	complaints = db.relationship('Complaint', backref = 'users', lazy = True)

	def __init__(self, firstname, lastname, username, category):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
		self.category = category
