from routes import db

class Status(db.Model):

    __tablename__ = 'status'

    status_id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer, nullable=False)
    status_meaning = db.Column(db.String(75), nullable=False)

    def __init__(self, status_code, status_meaning):
        self.status_code = status_code
        self.status_meaning = status_meaning
