from routes import db


#User model
class User(db.Model):
	
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75), nullable = False)
	lastname = db.Column(db.String(75), nullable = False)
	username = db.Column(db.String(75), unique = True, nullable = False)
	password = db.Column(db.String(100), nullable = False)
	category = db.Column(db.String(30), nullable = False)
	houses = db.relationship('House', backref = 'users', lazy = True)
	rental = db.relationship('Rental', backref = 'users', lazy = True)
	complaints = db.relationship('Complaint', backref = 'users', lazy = True)

	def __init__(self, firstname, lastname, username, password, category):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
		self.category = category
