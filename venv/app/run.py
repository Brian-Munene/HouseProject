from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import pymysql.cursors

from routes import app

if __name__ == "__main__":
	app.secret_key='secret123'
	app.run(debug=True)