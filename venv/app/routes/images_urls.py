from flask import Flask, session, logging, request, json, jsonify
from werkzeug.utils import secure_filename
import os
#file imports
from routes import app
from routes import db
from database.rental import Complaint
from database.rental import Image

ALLOWED_EXTENSIONS = set(['jpeg', 'png', 'jpg',])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS

@app.route('/InsertImage', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':
                file = request.files['file']
                #check if the reuest has the file part
                if 'file' not in request.files:
                        return('No file part')
                
                #if file not selected submit empty part without filename
                if file.filename == '':
                        return('No selected image')
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return('Image has been saved')



        
