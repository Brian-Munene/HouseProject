from routes import db


class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    tenant_name = db.Column(db.Integer, db.ForegnKey('tenants.tenant_id'), nullable=False)
    payment_type = db.Column(db.Integer, db.ForegnKey('payments.payment_id'), nullable=False)
    lease_id = db.Column(db.Integer, db.ForegnKey('leases.lease_id'), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_id, payment_id, lease_id, balance, public_id):
        self.public_id = public_id
        self.tenant_id = tenant_id
        self.payment_id = payment_id
        self.lease_id = lease_id
        self.balance = balance



