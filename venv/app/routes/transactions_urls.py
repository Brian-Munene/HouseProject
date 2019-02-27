from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
import arrow
import os
#file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.images import Image


#Insert transaction
# @app.route('/InsertTransaction', methods=['POST'])
# def insert
