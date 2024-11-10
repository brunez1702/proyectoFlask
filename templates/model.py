from flask_sqlalchemy import SQLAlchemy
from extensions import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(200))  # Nuevo campo
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

 # puesto emmpledo db; nombre del puesto y la descripcion de lo q hace en el puesto
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

# Función para inicializar los roles
def init_roles():
    if Role.query.count() == 0:  # Solo agrega roles si no existen
        roles = [
            {'name': 'Admin', 'description': 'Administrador del sistema'},
            {'name': 'Empleado', 'description': 'Empleado general'},
            {'name': 'Encargado', 'description': 'Encargado de supervisión'}
        ]
        # Agrega cada rol a la base de datos
        for role_data in roles:
            role = Role(name=role_data['name'], description=role_data['description'])
            db.session.add(role)
        db.session.commit()  # Guarda los cambios