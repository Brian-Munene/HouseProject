from passlib.apps import custom_app_context as pwd_context
from datetime import datetime, timedelta
import jwt

#file imports
from routes import db
from routes import app


#User model
class User(db.Model):

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    account_status = db.Column(db.Integer, nullable=False)

    # blocks = db.relationship('Block', backref='users', lazy=True)
    # rental = db.relationship('Rental', backref='users', lazy=True)
    # complaints = db.relationship('Complaint', backref='users', lazy=True)

    def __init__(self, email, category, account_status):
        self.category = category
        self.email = email
        self.account_status = account_status

'''
    def encode_auth_token(self, user_id):
        """"
        Generate the Auth Token
        :param user_id:
        :return: String
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validate the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'], 'utf-8')
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid Token. Please login again.'


class Token(db.Model):
    __tablename__ = 'Tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    token = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, nullable=True)
    scopes = db.Column(db.Text, nullable=True)
    revoked = db.Column(db.Integer, nullable=True)

    def __init__(self, user_id, client_id, scopes, revoked):
        self.user_id = user_id
        self.client_id = client_id
        self.scopes = scopes
        self.revoked = revoked


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens

    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        #Check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
'''