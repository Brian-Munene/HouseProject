from routes import db


class Landlord(db.Model):

    __tablename__ = 'landlords'

    landlord_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='landlords', lazy=True)

    def __init__(self, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
