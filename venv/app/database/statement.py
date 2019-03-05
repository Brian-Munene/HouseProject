from routes import db


class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    tenant_name = db.Column(db.String(75), nullable=False)
    payment_type = db.Column(db.String(75), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_name, payment_type, payment_amount, net_amount, public_id):
        self.public_id = public_id
        self.tenant_name = tenant_name
        self.payment_type = payment_type
        self.payment_amount = payment_amount
        self.net_amount = net_amount



