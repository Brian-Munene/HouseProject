from routes import db

class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key = True)
    image_url = db.Column(db.String(75), nullable = False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable = False)

    def __init__(self, image_id, image_url):
        self.image_url = image_url
