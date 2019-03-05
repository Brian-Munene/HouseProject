from routes import db
from datetime import datetime


class Lease(db.Model):

    __tablename__ = 'leases'

    lease_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    lease_begin_date = db.Column(db.Date, nullable=False)
    lease_end_date = db.Column(db.Date, nullable=False)
    lease_amount = db.Column(db.Float(12), nullable=False)
    promises = db.Column(db.Text(100), nullable=False)
    service_charges = db.Column(db.Float(12), nullable=True)
    notes = db.Column(db.Text(255), nullable=True)
    lease_status = db.Column(db.String(75), nullable=False)
    payment_interval = db.Column(db.Integer, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)

    # Relationships
    rentals = db.relationship('Rental', backref='leases', lazy=True)

    def __init__(self, tenant_id, unit_id, lease_begin_date, lease_end_date, lease_amount, promises, service_charges, notes, lease_status, paymnet_interval, public_id):
        self.tenant_id = tenant_id
        self.unit_id = unit_id
        self.public_id = public_id
        self.lease_begin_date = lease_begin_date
        self.lease_end_date = lease_end_date
        self.lease_amount = lease_amount
        self.promises = promises
        self.service_charges = service_charges
        self.notes = notes
        self.lease_status = lease_status
        self.payment_interval = paymnet_interval
