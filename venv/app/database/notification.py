from routes import db


class Notification(db.Model):

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    notification_message = db.Column(db.Text, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    notification_date = db.Column(db.Date, nullable=False)
    notification_type = db.Column(db.String(75), nullable=False)

    def __int__(self, notification_message, recipient_id, notification_date, notification_type, public_id):
        self.public_id = public_id
        self.notification_message = notification_message
        self.recipient_id = recipient_id
        self.notification_date = notification_date
        self.notification_type = notification_type
