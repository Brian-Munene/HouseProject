from datetime import datetime
from routes import db


#Unit Model
class Unit(db.Model):

    __tablename__ = 'units'

    unit_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.block_id'), nullable=True)
    unit_number = db.Column(db.String(25), nullable=False, unique=True)
    unit_status = db.Column(db.String(75), nullable=False)

    # Relationships
    rentals = db.relationship('Rental', backref='units', lazy=True)
    complaints = db.relationship('Complaint', backref='units', lazy=True)

    def __init__(self, block_id, unit_number, unit_status, public_id):
        self.public_id = public_id
        self.unit_number = unit_number
        self.block_id = block_id
        self.unit_status = unit_status



'''
class Block(db.Model):
    
    __tablename__ = 'blocks'

    block_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=True)
    block_name = db.Column(db.String(35), nullable=False)
    units = db.relationship('Unit', backref='units', lazy=True)
    
    def __init__(self, block_name, block_number, block_type):
        self.block_name = block_name
        self.block_number = block_number
        self.block_type = block_type
'''


