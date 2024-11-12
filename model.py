from datetime import datetime
from extensions import db  # Importar db desde extensions.py
from flask_login import UserMixin

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 

    def __repr__(self):
        return f'<Usuario id={self.id} nombre={self.nombre}>'

    def __str__(self):
        return self.nombre
    
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_producto.id'), nullable=False)

    categoria = db.relationship('CategoriaProducto', backref=db.backref('productos', lazy=True))

    def __repr__(self):
        return f'<Producto id={self.id} nombre={self.nombre} precio={self.precio} categoria_id={self.categoria_id}>'

    def __str__(self):
        return f'{self.nombre} - ${self.precio}'
    

class CategoriaProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<CategoriaProducto id={self.id} nombre={self.nombre}>'

    def __str__(self):
        return self.nombre
    
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref=db.backref('ventas', lazy=True))
    producto = db.relationship('Producto', backref=db.backref('ventas', lazy=True))

    def __repr__(self):
        return f'<Venta {self.id} - {self.cantidad} {self.producto.nombre}>'

    def __str__ (self):
        return f'Venta de {self.cantidad} unidades de {self.producto.nombre} por {self.usuario.nombre} el {self.fecha.strftime("%d/%m/%Y %H:%M")}'  

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Marca id={self.id} nombre={self.nombre}>'

    def __str__(self):
        return self.nombre

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    pais_origen = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Fabricante id={self.id} nombre={self.nombre} país={self.pais_origen}>'

    def __str__(self):
        return f'{self.nombre} ({self.pais_origen})'

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(100), nullable=False, unique=True)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)

    fabricante = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('modelos', lazy=True))

    def __repr__(self):
        return f'<Modelo id={self.id} nombre_modelo={self.nombre_modelo} fabricante_id={self.fabricante_id} marca_id={self.marca_id}>'

    def __str__(self):
        return f'{self.nombre_modelo} ({self.marca.nombre})'

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('caracteristicas', lazy=True))

    def __repr__(self):
        return f'<Caracteristica id={self.id} tipo={self.tipo} descripcion={self.descripcion} modelo_id={self.modelo_id}>'

    def __str__(self):
        return f'{self.tipo}: {self.descripcion}'

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))

    def __repr__(self):
        return f'<Equipo id={self.id} nombre={self.nombre} modelo_id={self.modelo_id} costo={self.costo} stock={self.stock}>'

    def __str__(self):
        return f'{self.nombre} - ${self.costo}'

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    ubicacion_almacen = db.Column(db.String(100), nullable=False)

    equipo = db.relationship('Equipo', backref=db.backref('stocks', lazy=True))

    def __repr__(self):
        return f'<Stock id={self.id} equipo_id={self.equipo_id} cantidad_disponible={self.cantidad_disponible} ubicacion_almacen={self.ubicacion_almacen}>'

    def __str__(self):
        return f'{self.cantidad_disponible} unidades de {self.equipo.nombre} en {self.ubicacion_almacen}'

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Proveedor id={self.id} nombre={self.nombre} contacto={self.contacto}>'

    def __str__(self):
        return f'{self.nombre} - Contacto: {self.contacto}'

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    compatible_con = db.Column(db.String(100), nullable=False)  # Ej. 'iPhone 14, Galaxy S21'

    def __repr__(self):
        return f'<Accesorio id={self.id} tipo={self.tipo} compatible_con={self.compatible_con}>'

    def __str__(self):
        return f'{self.tipo} - Compatible con: {self.compatible_con}'

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    salario = db.Column(db.Float, nullable=False)
    fecha_contratacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Empleado id={self.id} nombre={self.nombre} role={self.role.name} salario={self.salario}>'

    def __str__(self):
        return f'{self.nombre} - {self.role.name}'
    
 # puesto emmpledo db; nombre del puesto y la descripcion de lo q hace en el puesto
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)  # Nuevo campo para la descripción

    def __repr__(self):
        return f'<Role id={self.id} name={self.name} description={self.description}>'

    def __str__(self):
        return f'{self.name} - {self.description if self.description else "Sin descripción"}'


    # Función para inicializar los roles
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
        print("Roles inicializados correctamente.")
    else:
        print("Los roles ya están inicializados.")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(200))  # Nuevo campo
  