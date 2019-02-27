from routes import db
from datetime import datetime


class Complaint(db.Model):
    __tablename__ = 'complaints'
    complaint_id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text(75), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    fixed_date = db.Column(db.Date, nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)

    #Relationship with images table
    services = db.relationship('Services', backref='complaints', lazy=True)
    images = db.relationship('Image', backref='complaints', lazy=True)

    def __init__(self, message, due_date, fixed_date, unit_id):
        self.date_posted = datetime.now()
        self.message = message
        self.due_date = due_date
        self.fixed_date = fixed_date
        self.unit_id = unit_id

