from routes import db


class Block(db.Model):
    __tablename__ = 'blocks'

    block_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=True)
    block_name = db.Column(db.String(35), nullable=False)

    # Relationships
    units = db.relationship('Unit', backref='blocks', lazy=True)

    def __init__(self, building_name, building_number, building_type):
        self.building_name = building_name
        self.building_number = building_number
        self.building_type = building_type


#Property Model
class Property(db.Model):

    __tablename__ = 'property'

    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(75), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('property_managers.manager_id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.landlord_id'), nullable=False)

    # Relationships
    blocks = db.relationship('Block', backref='property', lazy=True)

    def __init__(self, property_name, property_manager_id, landlord_id):
        self.property_manager_id = property_manager_id
        self.property_name = property_name
        self.landlord_id = landlord_id


#property Manager Model
class PropertyManager(db.Model):

    __tablename__ = 'property_managers'

    manager_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='property_managers', lazy=True)

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Landlord's model
class Landlord(db.Model):

    __tablename__ = 'landlords'

    landlord_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='landlords', lazy=True)

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Caretaker Model
class Caretaker(db.Model):

    __tablename__ = 'caretakers'

    caretaker_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer,nullable=False, unique=True)

    def __init__(self, property_id, first_name, last_name, email, phone):
        self.property_id = property_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Tenant's Model
class Tenant(db.Model):

    __tablename__ = 'tenants'

    tenant_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)

    #Relationships
    rentals = db.relationship('Rental', backref='tenants', lazy=True)

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


#Transactions Model
class Transactions(db.Model):

    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    amount_paid = db.Column(db.Float(12), nullable=False)
    date_paid = db.Column(db.DateTime, nullable=False)

    def __init__(self, unit_id, amount_paid, date_paid):
        self.unit_id = unit_id
        self.amount_paid = amount_paid
        self.date_paid = date_paid


# Lease Model
class Lease(db.Model):

    __tablename__ = 'leases'

    lease_id = db.Column(db.Integer, primary_key=True)
    lease_begin_date = db.Column(db.DateTime, nullable=False)
    lease_end_date = db.Column(db.DateTime, nullable=False)
    lease_amount = db.Column(db.Float(12), nullable=False)
    promises = db.Column(db.Text(100), nullable=False)
    service_charges = db.Column(db.Float(12), nullable=True)
    notes = db.Column(db.Text(255), nullable=True)
    lease_status = db.Column(db.Integer, nullable=False)
    payment_interval = db.Column(db.Integer, nullable=False)

    # Relationships
    rentals = db.relationship('Rental', backref='leases', lazy=True)

    def __init__(self, lease_begin_date, lease_end_date, lease_amount, promises, service_charges, notes, lease_status, paymnet_interval):
        self.lease_begin_date = lease_begin_date
        self.lease_end_date = lease_end_date
        self.lease_amount = lease_amount
        self.promises = promises
        self.service_charges = service_charges
        self.notes = notes
        self.lease_status = lease_status
        self.payment_interval = paymnet_interval


# Status Model
class Status(db.Model):

    __tablename__ = 'status'

    status_id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer, nullable=False)
    status_meaning = db.Column(db.String(75), nullable=False)

    def __init__(self, status_code, status_meaning):
        self.status_code = status_code
        self.status_meaning = status_meaning


# Statement Model
class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_id, transaction_id, lease_id, balance):
        self.tenant_id = tenant_id
        self.transaction_id = transaction_id
        self.lease_id = lease_id
        self.balance = balance


# Service Providers model
class ServiceProviders(db.Model):

    __tablename__ = 'service_providers'

    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(75), nullable=False)
    provider_contact = db.Column(db.Integer, nullable=False, unique=True)

    #Relationships
    services = db.relationship('Services', backref='service_providers', lazy=True)

    def __init__(self, provider_name, provider_contact):
        self.provider_name = provider_name
        self.provider_contact = provider_contact


# Services Model
class Services(db.Model):

    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.provider_id'), nullable=False)
    fixed_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float(12), nullable=False)

    def __init__(self, complaint_id, provider_id, fixed_date, cost):
        self.complaint_id = complaint_id
        self.provider_id = provider_id
        self.fixed_date = fixed_date
        self.cost = cost


# Notifications Model
class Notification(db.Model):

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    notification_message = db.Column(db.Text(255), nullable=False)
    notification_recipient_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String(75), nullable=False)

    def __int__(self, notification_message, notification_recipient_id, notification_type):
        self.notification_message = notification_message
        self.notification_recipient_id = notification_recipient_id
        self.notification_type = notification_type
