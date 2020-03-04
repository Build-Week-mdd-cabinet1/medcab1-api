from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Strain_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    race = db.Column(db.String(50))
    flavors = db.Column(db.String(500))
    positive = db.Column(db.String(500))
    negative = db.Column(db.String(500))
    medical = db.Column(db.String(500))
    rating = db.Column(db.Float)
    description = db.Column(db.String(2000))
