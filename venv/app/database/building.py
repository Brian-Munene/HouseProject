from routes import db

class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(35), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    houses = db.relationship('Building', backref = 'buildings', lazy = True)
    
    def __init__(self, building_id, name, number):
        self.id = building_id
        self.name = name
        self.number = number
