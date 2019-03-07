from flask import Flask, session, g, logging, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from passlib.hash import sha256_crypt
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:motongoria@localhost:3306/plot'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


#Import routes
from routes import base_urls, unit_urls, rental_urls, user_urls, block_urls, complaint_urls, image_urls, property_urls, \
	notification_urls,service_provider_urls, payment_urls, landlord_urls, status_urls, caretaker_urls, payment_type_urls,\
	debt_urls