from routes import db


class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    tenant_name = db.Column(db.String(75), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForegnKey('tenants.tenant_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForegnKey('units.unit_id'), nullable=False)
    transaction_type = db.Column(db.String(75), nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_name, tenant_id, unit_id, transaction_type, transaction_amount, net_amount, transaction_date, public_id):
        self.public_id = public_id
        self.tenant_id = tenant_id
        self.unit_id = unit_id
        self.tenant_name = tenant_name
        self.payment_type = transaction_type
        self.payment_amount = transaction_amount
        self.transaction_date = transaction_date
        self.net_amount = net_amount



