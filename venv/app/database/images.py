from routes import db


#Images Model
class Image(db.Model):

    __tablename__ = 'complaints_images'

    image_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    image_name = db.Column(db.String(75), nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)

    def __init__(self, image_name, complaint_id, public_id):
        self.public_id = public_id
        self.image_name = image_name
        self.complaint_id = complaint_id
