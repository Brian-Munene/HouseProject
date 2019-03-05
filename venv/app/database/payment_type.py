from routes import db


class PaymentType(db.Model):

    __tablename__ = 'payment_types'

    type_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    type_code = db.Column(db.String(12), nullable=False, unique=True)
    type_meaning = db.Column(db.String(75), nullable=False, unique=True)

    def __init__(self, public_id, type_code, type_meaning):
        self.public_id = public_id
        self.type_code = type_code
        self.type_meaning = type_meaning
