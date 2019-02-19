from routes import db


class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForegnKey('tenants.tenant_id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForegnKey('transactions.transaction_id'), nullable=False)
    lease_id = db.Column(db.Integer, db.ForegnKey('leases.lease_id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_id, transaction_id, lease_id, balance):
        self.tenant_id = tenant_id
        self.transaction_id = transaction_id
        self.lease_id = lease_id
        self.balance = balance



