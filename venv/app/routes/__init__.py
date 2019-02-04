from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import pymysql.cursors


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:motongoria@localhost:3306/plot'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Import routes
from routes import base_urls, house_urls, rental_urls, user_urls