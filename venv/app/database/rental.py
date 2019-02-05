from routes import db

#rental Model
class Rental(db.Model):

	__tablename__ = 'rentals'

	rental_id = db.Column(db.Integer, primary_key = True)
	tenant_name = db.Column(db.String(75), unique = True)
	amount_paid = db.Column(db.Float(12))

	def __init__(self, tenant_name, amount_paid):
		self.tenant_name = tenant_name
		self.amount_paid = amount_paid