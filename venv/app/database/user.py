from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
#file imports
from routes import db
from routes import app


#User model
class User(db.Model):

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_access_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_access_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None #Token expired
        except BadSignature:
            return None #Invalid token
        user = User.query.get(data['id'])
        return user

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(75), nullable=False)
    lastname = db.Column(db.String(75), nullable=False)
    username = db.Column(db.String(75), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    houses = db.relationship('House', backref='users', lazy=True)
    rental = db.relationship('Rental', backref='users', lazy=True)
    complaints = db.relationship('Complaint', backref='users', lazy=True)

    def __init__(self, firstname, lastname, username, category):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.category = category
