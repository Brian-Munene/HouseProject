from routes import db


class Transactions(db.Model):

    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    amount_paid = db.Column(db.Float(12), nullable=False)
    date_paid = db.Column(db.Date, nullable=False)

    def __init__(self, unit_id, amount_paid, date_paid):
        self.unit_id = unit_id
        self.amount_paid = amount_paid
        self.date_paid = date_paid
