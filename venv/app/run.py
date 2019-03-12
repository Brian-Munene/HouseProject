from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
from flask_httpauth import HTTPBasicAuth

from routes import app

auth = HTTPBasicAuth()

if __name__ == "__main__":
	app.config['SECRET_KEY'] = 'fluidtech2propertymanagement'
	app.run(debug=True, port=7001)

