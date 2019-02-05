from routes import db


#User model
class User(db.Model):
	
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75))
	lastname = db.Column(db.String(75))
	username = db.Column(db.String(75), unique = True)
	password = db.Column(db.String(100))
	houses = db.relationship('House', backref = 'users', lazy = True)
	rental = db.relationship('Rental', backref = 'users', lazy = True)
	complaints = db.relationship('Complaint', backref = 'users', lazy = True)

	def __init__(self, firstname, lastname, username, password):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
