from routes import db

class Building(db.Model):
    
    __tablename__ = 'buildings'

    building_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(35), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    building_type = db.Column(db.String(35), nullable = False)
    houses = db.relationship('House', backref = 'buildings', lazy = True)
    
    def __init__(self, name, number, building_type):
        self.name = name
        self.number = number
        self.building_type = building_type
