from flask import Flask, session, logging, send_from_directory, request, json, jsonify
from werkzeug.utils import secure_filename
import os
#file imports
from routes import app
from routes import db
from database.rental import Complaint
from database.rental import Image

ALLOWED_EXTENSIONS = set(['jpeg', 'png', 'jpg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS


@app.route('/InsertImage', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':

                #check if the request has the file part
                image = request.files['image']
                #if file not selected submit empty part without filename
                if image.filename == '':
                        return('No selected image')
                if image and allowed_file(image.filename):
                        image_name = secure_filename(image.filename)
                        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                        app.logger.info("saving {}".format(saved_path))
                        image.save(saved_path)
                        path = app.config['UPLOAD_FOLDER'] + image_name

                        #complaint_id = 1
                        #image_details = Image(path, complaint_id)
                        #db.session.add(image_details)

                        db.session.commit()
                        return send_from_directory(app.config['UPLOAD_FOLDER'], image_name, as_attachment=True)
