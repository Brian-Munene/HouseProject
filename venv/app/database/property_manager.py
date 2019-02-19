from routes import db


class PropertyManager(db.Model):

    __tablename__ = 'property_managers'

    manager_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.integer(12), nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='property_managers', lazy=True)

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
