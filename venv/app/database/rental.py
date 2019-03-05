from datetime import datetime
import arrow
from routes import db


#rental Model
class Rental(db.Model):

    __tablename__ = 'rentals'
    
    rental_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    tenant_name = db.Column(db.String(75), nullable=False)
    unit_number = db.Column(db.String(25), nullable=False)
    lease_end_date = db.Column(db.Date, nullable=False)
    
    def __init__(self, tenant_name, unit_number, lease_end_date, public_id):
        self.public_id = public_id
        self.tenant_name = tenant_name
        self.unit_number = unit_number
        self.lease_end_date = lease_end_date

'''
#Complaint Model

class Complaint(db.Model):
    __tablename__ = 'complaints'
    complaint_id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text(75), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    fixed_date = db.Column(db.DateTime, nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    #Relationship with images table
    images = db.relationship('Image', backref='complaints', lazy=True)

    def __init__(self, message, due_date, fixed_date, unit_id):
        self.date_posted = datetime.now()
        self.message = message
        self.due_date = due_date
        self.fixed_date = fixed_date
        self.unit_id = unit_id




#Images Model
class Image(db.Model):

    __tablename__ = 'complaints_images'

    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(75), nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)

    def __init__(self, image_name, complaint_id):
        self.image_name = image_name
        self.complaint_id = complaint_id 
'''