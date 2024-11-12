
from marshmallow import Schema, fields
from datetime import datetime

class UsuarioSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True) 


class ProductoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    precio = fields.Float(required=True)
    cantidad = fields.Int(required=True)
    categoria = fields.Nested('CategoriaProductoSchema', only=['id', 'nombre'])

class CategoriaProductoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    descripcion = fields.Str()


class VentaSchema(Schema):
    id = fields.Int()
    usuario = fields.Nested(UsuarioSchema, only=['id', 'nombre'])
    producto = fields.Nested(ProductoSchema, only=['id', 'nombre'])
    cantidad = fields.Int(required=True)
    fecha = fields.DateTime(format='%Y-%m-%d %H:%M:%S', default=datetime.utcnow)


class MarcaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)


class FabricanteSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    pais_origen = fields.Str(required=True)

class ModeloSchema(Schema):
    id = fields.Int()
    nombre_modelo = fields.Str(required=True)
    fabricante = fields.Nested(FabricanteSchema, only=['id', 'nombre'])
    marca = fields.Nested(MarcaSchema, only=['id', 'nombre'])


class CaracteristicaSchema(Schema):
    id = fields.Int()
    tipo = fields.Str(required=True)
    descripcion = fields.Str(required=True)
    modelo = fields.Nested(ModeloSchema, only=['id', 'nombre_modelo'])


class EquipoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    modelo = fields.Nested(ModeloSchema, only=['id', 'nombre_modelo'])
    costo = fields.Float(required=True)
    stock = fields.Int(required=True)

class StockSchema(Schema):
    id = fields.Int()
    equipo = fields.Nested(EquipoSchema, only=['id', 'nombre'])
    cantidad_disponible = fields.Int(required=True)
    ubicacion_almacen = fields.Str(required=True)


class ProveedorSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    contacto = fields.Str(required=True)


class AccesorioSchema(Schema):
    id = fields.Int()
    tipo = fields.Str(required=True)
    compatible_con = fields.Str(required=True)


class EmpleadoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    role = fields.Nested('RoleSchema', only=['id', 'name'])
    salario = fields.Float(required=True)
    fecha_contratacion = fields.DateTime(format='%Y-%m-%d %H:%M:%S', default=datetime.utcnow)

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str()


