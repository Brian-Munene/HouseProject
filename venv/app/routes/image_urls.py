from flask import Flask, session, logging, send_from_directory, send_file, request, json, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import arrow
import uuid
import os
#file imports
from routes import app
from routes import db
from database.complaint import Complaint
from database.images import Image

ALLOWED_EXTENSIONS = set(['jpeg', 'png', 'jpg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS


#Insert Image using complaint's public_id
@app.route('/InsertImage/<public_id>', methods=['POST'])
def upload_file(public_id):
        if request.method == 'POST':

                #check if the request has the file part
                image = request.files['image']
                #if file not selected submit empty part without filename
                if image.filename == '':
                        return jsonify({'message': 'No selected image'}), 400
                if image and allowed_file(image.filename):
                        a = arrow.utcnow().timestamp
                        image_name = str(a) + secure_filename(image.filename)
                        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                        app.logger.info("saving {}".format(saved_path))
                        image.save(saved_path)
                        path = app.config['UPLOAD_FOLDER'] + image_name
                        complaint = Complaint.query.filter_by(public_id=public_id).first()
                        image_public_id = str(uuid.uuid4())
                        image_details = Image(path, complaint.complaint_id, image_public_id)
                        db.session.add(image_details)
                        db.session.commit()
                        response_object = {
                                'path': path,
                                'image-name': image_name
                                }
                        return jsonify(response_object)
                else:
                        return jsonify({'data': 'Error sending from directory'}), 400


#View Complaint Images using complaint's public_id
@app.route('/ViewImages/<public_id>')
def view_images(public_id):
        complaint = Complaint.query.filter_by(public_id=public_id).first()
        images = Image.query.filter_by(complaint_id=complaint.complaint_id).all()
        images_list = []
        for image in images:
            filename = image.image_name
            # fp = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            # file = FileStorage(fp)
            # send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
            # url = "file:///C:/Users/Brian/Documents/Flask/BlockProject/venv/app/uploads/" + filename
            # print (url)
            # images_list.append(file)
            images_list.append(filename)

        return jsonify(images_list)




