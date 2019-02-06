from routes import db
from datetime import datetime

class Complaint(db.Model):
    __tablename__ = 'complaints'
    date_posted = db.Column(db.DateTime, nullable = False)
    complaint_id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text(75), nullable = False)
    due_date = db.Column(db.DateTime, nullable = True)
    fixed_date = db.Column(db.DateTime, nullable = True)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    #Relationship with images table
    images = db.relationship('Image', backref = 'complaints', lazy = True)

    def __init__(self, date_posted, message, due_date, fixed_date):
        self.date_posted = date_posted
        self.message = message
        self.due_date = due_date
        self.fixed_date = fixed_date
