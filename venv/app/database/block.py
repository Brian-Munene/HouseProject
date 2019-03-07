from datetime import datetime
from routes import db


class Block(db.Model):
    __tablename__ = 'blocks'

    block_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    block_name = db.Column(db.String(35), nullable=False)
    number_of_units = db.Column(db.Integer, nullable=False)

    # Relationships
    units = db.relationship('Unit', backref='blocks', lazy=True)

    def __init__(self, property_id, block_name, number_of_units, public_id):
        self.number_of_units = number_of_units
        self.public_id = public_id
        self.property_id = property_id
        self.block_name = block_name


#Property Model
class Property(db.Model):

    __tablename__ = 'property'

    property_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    property_name = db.Column(db.String(75), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('property_managers.manager_id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.landlord_id'), nullable=False)

    # Relationships
    blocks = db.relationship('Block', backref='property', lazy=True)

    def __init__(self, property_name, manager_id, landlord_id, public_id):
        self.public_id = public_id
        self.manager_id = manager_id
        self.property_name = property_name
        self.landlord_id = landlord_id


#property Manager Model
class PropertyManager(db.Model):

    __tablename__ = 'property_managers'

    manager_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='property_managers', lazy=True)

    def __init__(self, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Landlord's model
class Landlord(db.Model):

    __tablename__ = 'landlords'

    landlord_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    # Relationships
    properties = db.relationship('Property', backref='landlords', lazy=True)

    def __init__(self, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Caretaker Model
class Caretaker(db.Model):

    __tablename__ = 'caretakers'

    caretaker_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    def __init__(self, property_id, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.property_id = property_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


# Tenant's Model
class Tenant(db.Model):

    __tablename__ = 'tenants'

    tenant_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)

    #Relationships
    leases = db.relationship('Lease', backref='tenants', lazy=True)

    def __init__(self, first_name, last_name, email, phone, public_id):
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


#Payments Model
class Payment(db.Model):

    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    amount_paid = db.Column(db.Float(12), nullable=False)
    payment_type = db.Column(db.String(30), nullable=False)
    debt_id = db.Column(db.Integer, db.ForeignKey('debts.debt_id'), nullable=False)
    date_paid = db.Column(db.Date, nullable=False)

    def __init__(self, unit_id, amount_paid, payment_type, debt_id, public_id):
        self.public_id = public_id
        self.debt_id = debt_id
        self.unit_id = unit_id
        self.amount_paid = amount_paid
        self.payment_type = payment_type
        self.date_paid = datetime.utcnow()


#Debt Model
class Debt(db.Model):
    __tablename__ = 'debts'

    debt_id = db.Column(db.Integer, nullable=False, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    bill_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False, default=0)
    debt_status = db.Column(db.String(75), nullable=False)
    debt_date = db.Column(db.DateTime, nullable=False)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=False)
    #Relationships
    payments = db.relationship('Payment', backref='debts', lazy=True)

    def __init__(self, bill_amount, paid_amount, debt_status, debt_date, lease_id, public_id):
        self.public_id = public_id
        self.bill_amount = bill_amount
        self.paid_amount = paid_amount
        self.debt_status = debt_status
        self.lease_id = lease_id
        self.debt_date = debt_date


# Lease Model
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
    debts = db.relationship('Debt', backref='leases', lazy=True)

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

# Status Model
class Status(db.Model):

    __tablename__ = 'status'

    status_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    status_code = db.Column(db.Integer, nullable=False, unique=True)
    status_meaning = db.Column(db.String(75), nullable=False, unique=True)

    def __init__(self, status_code, status_meaning, public_id):
        self.public_id = public_id
        self.status_code = status_code
        self.status_meaning = status_meaning


# Statement Model
class Statement(db.Model):

    __tablename__ = 'statements'

    statement_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    tenant_name = db.Column(db.String(75), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    transaction_type = db.Column(db.String(75), nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)

    def __init__(self, tenant_id, unit_id, tenant_name, transaction_type, transaction_amount, net_amount, transaction_date, public_id):
        self.public_id = public_id
        self.tenant_id = tenant_id
        self.unit_id = unit_id
        self.tenant_name = tenant_name
        self.transaction_type = transaction_type
        self.transaction_amount = transaction_amount
        self.transaction_date = transaction_date
        self.net_amount = net_amount


# Service Providers model
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


# Services Model
class Services(db.Model):

    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.provider_id'), nullable=False)
    fixed_date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float(12), nullable=False)

    def __init__(self, complaint_id, provider_id, cost, public_id):
        self.public_id = public_id
        self.complaint_id = complaint_id
        self.provider_id = provider_id
        self.fixed_date = datetime.now()
        self.cost = cost


# Notifications Model
class Notification(db.Model):

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    notification_message = db.Column(db.Text(255), nullable=False)
    notification_recipient_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String(75), nullable=False)

    def __int__(self, notification_message, notification_recipient_id, notification_type, public_id):
        self.public_id = public_id
        self.notification_message = notification_message
        self.notification_recipient_id = notification_recipient_id
        self.notification_type = notification_type


class PaymentType(db.Model):
    __tablename__ = 'payment_types'

    type_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    type_code = db.Column(db.String(12), nullable=False, unique=True)
    type_meaning = db.Column(db.String(75), nullable=False, unique=True)

    def __init__(self, public_id, type_code, type_meaning):
        self.public_id = public_id
        self.type_code = type_code
        self.type_meaning = type_meaning

