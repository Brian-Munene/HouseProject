from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
import cherrypy
from flask_httpauth import HTTPBasicAuth

from routes import app

auth = HTTPBasicAuth()

cherrypy.tree.graft(app.wsgi_app, '/')
cherrypy.config.update({'server.socket_host': '127.0.0.1',
						   'server.socket_port': 7001,
						   'engine.autoreload.on': False,
						   })

if __name__ == "__main__":
	app.config['SECRET_KEY'] = 'fluidtech2propertymanagement'
	cherrypy.engine.start()
	# app.run(debug=True, port=7001)
