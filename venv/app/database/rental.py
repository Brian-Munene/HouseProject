from routes import db

#rental Model
class Rental(db.Model):

	__tablename__ = 'rentals'

	id = db.Column(db.Integer, primary_key = True)
	tenant_name = db.Column(db.String(75), unique = True, nullable = False)
	amount_paid = db.Column(db.Float(12), nullable = False)
	paid_at = db.Column(db.DateTime, nullable = False)
	house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

	def __init__(self, tenant_name, amount_paid, paid_at):
		self.tenant_name = tenant_name
		self.amount_paid = amount_paid
		self.paid_at = paid_at