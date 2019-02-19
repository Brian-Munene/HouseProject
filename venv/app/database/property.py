from routes import db


class Property(db.Model):

    __tablename__ = 'property'

    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(75), nullable=False)
    property_manager_id = db.Column(db.Integer, db.ForeignKey('property_managers.property_manager_id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.landlord_id'), nullable=False)

    # Relationships
    blocks = db.relationship('Block', backref='property', lazy=True)

    def __init__(self, property_name, property_manager_id, landlord_id):
        self.property_manager_id = property_manager_id
        self.property_name = property_name
        self.landlord_id = landlord_id
