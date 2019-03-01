from routes import db


class ServiceProviders(db.Model):

    __tablename__ = 'service_providers'

    provider_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    provider_name = db.Column(db.String(75), nullable=False)
    provider_contact = db.Column(db.String(15), nullable=False, unique=True)

    #Relationships
    services = db.relationship('Services', backref='service_providers', lazy=True)

    def __init__(self, provider_name, provider_contact, public_id):
        self.public_id = public_id
        self.provider_name = provider_name
        self.provider_contact = provider_contact
