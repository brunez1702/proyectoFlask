from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(200))  # Nuevo campo


    class Item(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         name = db.Column(db.String(100), nullable=False)
         description = db.Column(db.Text, nullable=True)