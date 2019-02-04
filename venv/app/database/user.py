from routes import db


#User model
class User(db.Model):
	
	__tablename__ = 'users'

	userId = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75))
	lastname = db.Column(db.String(75))
	username = db.Column(db.String(75))
	password = db.Column(db.String(100))

	def __init__(self, firstname, lastname, username, password):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
