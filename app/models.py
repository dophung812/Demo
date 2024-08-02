from . import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    follow = db.Column(db.Integer, nullable=False)
