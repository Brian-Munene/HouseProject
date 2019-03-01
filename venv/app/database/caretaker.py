from routes import db


# Caretaker Model
class Caretaker(db.Model):

    __tablename__ = 'caretakers'

    caretaker_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    def __init__(self, property_id, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.property_id = property_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
