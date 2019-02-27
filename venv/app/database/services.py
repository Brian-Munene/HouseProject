from routes import db


class Services(db.Model):

    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.provider_id'), nullable=False)
    fixed_date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float(12), nullable=False)

    def __init__(self, complaint_id, provider_id, fixed_date, cost):
        self.complaint_id = complaint_id
        self.provider_id = provider_id
        self.fixed_date = fixed_date
        self.cost = cost
