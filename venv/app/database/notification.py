from routes import db


class Notification(db.Model):

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    notification_message = db.Column(db.Text(255), nullable=False)
    notification_recipient_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String(75), nullable=False)

    def __int__(self, notification_message, notification_recipient_id, notification_type):
        self.notification_message = notification_message
        self.notification_recipient_id = notification_recipient_id
        self.notification_type = notification_type
