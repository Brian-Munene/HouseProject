from datetime import datetime
from routes import db


#Debt Model
class Debt(db.Model):
    __tablename__ = 'debts'

    debt_id = db.Column(db.Integer, nullable=False, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    bill_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False, default=0)
    debt_status = db.Column(db.String(75), nullable=False)
    debt_date = db.Column(db.Date, nullable=False)
    #Relationships
    payments = db.relationship('Payment', backref='debts', lazy=True)

    def __init__(self, bill_amount, paid_amount, debt_status, public_id):
        self.public_id = public_id
        self.bill_amount = bill_amount
        self.paid_amount = paid_amount
        self.debt_status = debt_status
        self.debt_date = datetime.utcnow()
