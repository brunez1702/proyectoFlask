from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from extensions import db
from model import   Usuario, Producto, CategoriaProducto, Marca, Fabricante, Modelo, Caracteristica, Equipo, Stock, Proveedor, Accesorio, Empleado
from schemas import UsuarioSchema, ProductoSchema, CategoriaProductoSchema, MarcaSchema, FabricanteSchema, ModeloSchema, CaracteristicaSchema, EquipoSchema, VentaSchema, EmpleadoSchema, StockSchema, ProveedorSchema, AccesorioSchema
from flask_jwt_extended import  jwt_required, get_jwt_identity, create_access_token
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

# Crear un Blueprint para las rutas de la API
api = Blueprint('api', __name__)


# Función para verificar si el usuario es Admin
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()  # Obtenemos la identidad del JWT
        user = Usuario.query.filter_by(nombre=current_user).first()
        if user and user.role == 'Admin':
            return fn(*args, **kwargs)
        else:
            return jsonify({"message": "Acceso no autorizado"}), 403
    return wrapper

# Endpoint para obtener todos los objetos de Item (sin restricción)
@api.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    result = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
    return jsonify(result)

# Endpoint para crear un objeto nuevo (solo Admin)
@api.route('/items', methods=['POST'])
@jwt_required()
@admin_required  
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Objeto creado exitosamente"}), 201

# Ruta de login para autenticación con JWT
@api.route('/login-api', methods=['POST'])
def login_api():
    data = request.get_json()  
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Faltan credenciales"}), 400  # Validación de datos

    # Buscar al usuario por el nombre de usuario
    user = Usuario.query.filter_by(nombre=username).first()

    if user and check_password_hash(user.password, password):  # Verificar la contraseña
        # Generar token JWT con expiración de 15 minutos
        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=15))
        return jsonify({
            'access_token': access_token,
            'username': user.nombre  # También puedes devolver el nombre del usuario
        }), 200  # Retornar el token y éxito

    return jsonify({"message": "El usuario o la contraseña son incorrectos"}), 401  # Respuesta de error

# Ruta para obtener todos los usuarios (API)
@api.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    usuarios = Usuario.query.all()
    result = UsuarioSchema.dump(usuarios)  
    return jsonify(result), 200

# Ruta para agregar un nuevo usuario (solo Admin)
@api.route('/usuarios', methods=['POST'])
@jwt_required()
@admin_required 
def add_usuario():
    data = request.get_json()
    UsuarioSchema = UsuarioSchema()

    errors = UsuarioSchema.validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_usuario = UsuarioSchema.load(data)
    usuario = Usuario(
        nombre=nuevo_usuario['nombre'],
        email=nuevo_usuario['email'],
        password=nuevo_usuario['password']
    )

    db.session.add(usuario)
    db.session.commit()
    return UsuarioSchema.jsonify(nuevo_usuario), 201

# Ruta para editar un usuario (solo Admin)
@api.route('/usuarios/editar/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required  
def edit_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get_or_404(id)
    usuario_schema = UsuarioSchema(partial=True)

    # Validar datos
    errors = usuario_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualizar datos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'email' in data:
        usuario.email = data['email']
    if 'password' in data:
        usuario.password = data['password']

    db.session.commit()
    return jsonify({"message": "Usuario actualizado correctamente"}), 200


# Ruta para eliminar un usuario (solo Admin)
@api.route('/usuarios/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required  
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"}), 200


# Ruta para obtener todos los productos
@api.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    productos = Producto.query.all()
    result = ProductoSchema(many=True).dump(productos)
    return jsonify(result), 200

# Ruta para crear un nuevo producto (solo Admin)
@api.route('/productos', methods=['POST'])
@jwt_required()
@admin_required
def crear_producto():
    data = request.get_json()
    errors = ProductoSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_producto = ProductoSchema().load(data)
    db.session.add(nuevo_producto)
    db.session.commit()

    return ProductoSchema().jsonify(nuevo_producto), 201

# Ruta para editar un producto existente (solo Admin)
@api.route('/productos/editar/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()
    
    errors = ProductoSchema().validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    producto.nombre = data.get('nombre', producto.nombre)
    producto.precio = data.get('precio', producto.precio)
    producto.cantidad = data.get('cantidad', producto.cantidad)
    producto.categoria_id = data.get('categoria_id', producto.categoria_id)

    db.session.commit()
    return ProductoSchema().jsonify(producto), 200

# Ruta para eliminar un producto (solo Admin)
@api.route('/productos/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado con éxito"}), 200

# Obtener todas las categorías de productos
@api.route('/categorias', methods=['GET'])
@jwt_required()
def get_categorias():
    categorias = CategoriaProducto.query.all()
    result = CategoriaProductoSchema(many=True).dump(categorias)
    return jsonify(result), 200

# Crear una nueva categoría de producto
@api.route('/categorias', methods=['POST'])
@jwt_required()
@admin_required
def crear_categoria():
    data = request.get_json()
    errors = CategoriaProductoSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_categoria = CategoriaProductoSchema().load(data)
    db.session.add(nueva_categoria)
    db.session.commit()

    return CategoriaProductoSchema().jsonify(nueva_categoria), 201

# Editar una categoría de producto
@api.route('/categorias/editar/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_categoria(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    data = request.get_json()

    errors = CategoriaProductoSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    categoria.nombre = data.get('nombre', categoria.nombre)
    categoria.descripcion = data.get('descripcion', categoria.descripcion)

    db.session.commit()
    return CategoriaProductoSchema().jsonify(categoria), 200

# Eliminar una categoría de producto
@api.route('/categorias/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_categoria(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoría eliminada con éxito"}), 200

# Obtener todas las ventas
@api.route('/ventas', methods=['GET'])
@jwt_required()
def get_ventas():
    ventas = Venta.query.all()
    result = VentaSchema(many=True).dump(ventas)
    return jsonify(result), 200

# Crear una nueva venta
@api.route('/ventas', methods=['POST'])
@jwt_required()
@admin_required
def crear_venta():
    data = request.get_json()
    errors = VentaSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_venta = VentaSchema().load(data)
    db.session.add(nueva_venta)
    db.session.commit()

    return VentaSchema().jsonify(nueva_venta), 201

# Editar una venta existente
@api.route('/ventas/editar/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    data = request.get_json()

    errors = VentaSchema().validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    venta.usuario_id = data.get('usuario_id', venta.usuario_id)
    venta.producto_id = data.get('producto_id', venta.producto_id)
    venta.cantidad = data.get('cantidad', venta.cantidad)

    db.session.commit()
    return VentaSchema().jsonify(venta), 200

# Eliminar una venta
@api.route('/ventas/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"message": "Venta eliminada con éxito"}), 200

# Obtener todas las marcas
@api.route('/marcas', methods=['GET'])
@jwt_required()
def get_marcas():
    marcas = Marca.query.all()
    result = MarcaSchema(many=True).dump(marcas)
    return jsonify(result), 200

# Crear una nueva marca
@api.route('/marcas', methods=['POST'])
@jwt_required()
@admin_required
def crear_marca():
    data = request.get_json()
    errors = MarcaSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_marca = MarcaSchema().load(data)
    db.session.add(nueva_marca)
    db.session.commit()

    return MarcaSchema().jsonify(nueva_marca), 201

# Editar una marca
@api.route('/marcas/editar/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    data = request.get_json()

    errors = MarcaSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'nombre' in data:
        marca.nombre = data['nombre']

    db.session.commit()
    return jsonify({"message": "Marca actualizada con éxito"}), 200

# Eliminar una marca
@api.route('/marcas/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    return jsonify({"message": "Marca eliminada con éxito"}), 200


# Obtener todos los fabricantes
@api.route('/fabricantes', methods=['GET'])
def lista_fabricantes():
    fabricantes = Fabricante.query.all()
    result = FabricanteSchema(many=True).dump(fabricantes)
    return jsonify(result), 200

# Crear un nuevo fabricante
@api.route('/fabricantes', methods=['POST'])
@jwt_required()
@admin_required
def crear_fabricante():
    data = request.get_json()
    errors = FabricanteSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_fabricante = FabricanteSchema().load(data)
    db.session.add(nuevo_fabricante)
    db.session.commit()

    return FabricanteSchema().jsonify(nuevo_fabricante), 201

# Editar un fabricante existente
@api.route('/fabricantes/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    data = request.get_json()

    errors = FabricanteSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'nombre' in data:
        fabricante.nombre = data['nombre']
    if 'pais_origen' in data:
        fabricante.pais_origen = data['pais_origen']

    db.session.commit()
    return jsonify({"message": "Fabricante actualizado con éxito"}), 200

# Eliminar un fabricante
@api.route('/fabricantes/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    return jsonify({"message": "Fabricante eliminado con éxito"}), 200



# Obtener todos los modelos
@api.route('/modelos', methods=['GET'])
def lista_modelos():
    modelos = Modelo.query.all()
    result = ModeloSchema(many=True).dump(modelos)
    return jsonify(result), 200

# Crear un nuevo modelo
@api.route('/modelos', methods=['POST'])
@jwt_required()
@admin_required
def crear_modelo():
    data = request.get_json()
    errors = ModeloSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_modelo = ModeloSchema().load(data)
    db.session.add(nuevo_modelo)
    db.session.commit()

    return ModeloSchema().jsonify(nuevo_modelo), 201

# Editar un modelo existente
@api.route('/modelos/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    data = request.get_json()

    errors = ModeloSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'nombre_modelo' in data:
        modelo.nombre_modelo = data['nombre_modelo']
    if 'fabricante_id' in data:
        modelo.fabricante_id = data['fabricante_id']
    if 'marca_id' in data:
        modelo.marca_id = data['marca_id']

    db.session.commit()
    return jsonify({"message": "Modelo actualizado con éxito"}), 200

# Eliminar un modelo
@api.route('/modelos/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    return jsonify({"message": "Modelo eliminado con éxito"}), 200


# Obtener todas las características
@api.route('/caracteristicas', methods=['GET'])
def lista_caracteristicas():
    caracteristicas = Caracteristica.query.all()
    result = CaracteristicaSchema(many=True).dump(caracteristicas)
    return jsonify(result), 200

# Crear una nueva característica
@api.route('/caracteristicas', methods=['POST'])
@jwt_required()
@admin_required
def crear_caracteristica():
    data = request.get_json()
    errors = CaracteristicaSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_caracteristica = CaracteristicaSchema().load(data)
    db.session.add(nueva_caracteristica)
    db.session.commit()

    return CaracteristicaSchema().jsonify(nueva_caracteristica), 201

# Editar una característica existente
@api.route('/caracteristicas/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    data = request.get_json()

    errors = CaracteristicaSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'tipo' in data:
        caracteristica.tipo = data['tipo']
    if 'descripcion' in data:
        caracteristica.descripcion = data['descripcion']
    if 'modelo_id' in data:
        caracteristica.modelo_id = data['modelo_id']

    db.session.commit()
    return jsonify({"message": "Característica actualizada con éxito"}), 200

# Eliminar una característica
@api.route('/caracteristicas/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return jsonify({"message": "Característica eliminada con éxito"}), 200



# Obtener todos los equipos
@api.route('/equipos', methods=['GET'])
def lista_equipos():
    equipos = Equipo.query.all()
    result = EquipoSchema(many=True).dump(equipos)
    return jsonify(result), 200

# Crear un nuevo equipo
@api.route('/equipos', methods=['POST'])
@jwt_required()
@admin_required
def crear_equipo():
    data = request.get_json()
    errors = EquipoSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_equipo = EquipoSchema().load(data)
    db.session.add(nuevo_equipo)
    db.session.commit()

    return EquipoSchema().jsonify(nuevo_equipo), 201

# Editar un equipo existente
@api.route('/equipos/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    data = request.get_json()

    errors = EquipoSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'nombre' in data:
        equipo.nombre = data['nombre']
    if 'modelo_id' in data:
        equipo.modelo_id = data['modelo_id']
    if 'costo' in data:
        equipo.costo = data['costo']
    if 'stock' in data:
        equipo.stock = data['stock']

    db.session.commit()
    return jsonify({"message": "Equipo actualizado con éxito"}), 200

# Eliminar un equipo
@api.route('/equipos/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return jsonify({"message": "Equipo eliminado con éxito"}), 200



# Obtener todos los stocks
@api.route('/stocks', methods=['GET'])
def lista_stocks():
    stocks = Stock.query.all()
    result = StockSchema(many=True).dump(stocks)
    return jsonify(result), 200

# Crear un nuevo stock
@api.route('/stocks', methods=['POST'])
@jwt_required()
@admin_required
def crear_stock():
    data = request.get_json()
    errors = StockSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_stock = StockSchema().load(data)
    db.session.add(nuevo_stock)
    db.session.commit()

    return StockSchema().jsonify(nuevo_stock), 201

# Editar un stock existente
@api.route('/stocks/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_stock(id):
    stock = Stock.query.get_or_404(id)
    data = request.get_json()

    errors = StockSchema(partial=True).validate(data)
    if errors:
        return jsonify(errors), 400

    if 'equipo_id' in data:
        stock.equipo_id = data['equipo_id']
    if 'cantidad_disponible' in data:
        stock.cantidad_disponible = data['cantidad_disponible']
    if 'ubicacion_almacen' in data:
        stock.ubicacion_almacen = data['ubicacion_almacen']

    db.session.commit()
    return jsonify({"message": "Stock actualizado con éxito"}), 200

# Eliminar un stock
@api.route('/stocks/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock eliminado con éxito"}), 200



# Obtener todos los proveedores
@api.route('/proveedores', methods=['GET'])
@jwt_required()
def obtener_proveedores():
    proveedores = Proveedor.query.all()
    resultado = ProveedorSchema(many=True).dump(proveedores)
    return jsonify(resultado), 200

# Crear un proveedor
@api.route('/proveedores', methods=['POST'])
@jwt_required()
@admin_required
def crear_proveedor():
    datos = request.get_json()
    errors = ProveedorSchema().validate(datos)
    if errors:
        return jsonify(errors), 400

    nuevo_proveedor = ProveedorSchema().load(datos)
    db.session.add(nuevo_proveedor)
    db.session.commit()
    
    return ProveedorSchema().jsonify(nuevo_proveedor), 201

# Editar un proveedor
@api.route('/proveedores/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    datos = request.get_json()

    errors = ProveedorSchema(partial=True).validate(datos)
    if errors:
        return jsonify(errors), 400

    if 'nombre' in datos:
        proveedor.nombre = datos['nombre']
    if 'contacto' in datos:
        proveedor.contacto = datos['contacto']

    db.session.commit()
    
    return ProveedorSchema().jsonify(proveedor), 200

# Eliminar un proveedor
@api.route('/proveedores/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    
    return jsonify({"message": "Proveedor eliminado con éxito"}), 200


# Obtener todos los accesorios
@api.route('/accesorios', methods=['GET'])
@jwt_required()
def obtener_accesorios():
    accesorios = Accesorio.query.all()
    resultado = AccesorioSchema(many=True).dump(accesorios)
    return jsonify(resultado), 200

# Crear un accesorio
@api.route('/accesorios', methods=['POST'])
@jwt_required()
@admin_required
def crear_accesorio():
    datos = request.get_json()
    errors = AccesorioSchema().validate(datos)
    if errors:
        return jsonify(errors), 400

    nuevo_accesorio = AccesorioSchema().load(datos)
    db.session.add(nuevo_accesorio)
    db.session.commit()
    
    return AccesorioSchema().jsonify(nuevo_accesorio), 201

# Editar un accesorio
@api.route('/accesorios/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    datos = request.get_json()

    errors = AccesorioSchema(partial=True).validate(datos)
    if errors:
        return jsonify(errors), 400

    if 'tipo' in datos:
        accesorio.tipo = datos['tipo']
    if 'compatible_con' in datos:
        accesorio.compatible_con = datos['compatible_con']

    db.session.commit()
    
    return AccesorioSchema().jsonify(accesorio), 200

# Eliminar un accesorio
@api.route('/accesorios/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    db.session.delete(accesorio)
    db.session.commit()
    
    return jsonify({"message": "Accesorio eliminado con éxito"}), 200


# Obtener todos los empleados
@api.route('/empleados', methods=['GET'])
@jwt_required()
def obtener_empleados():
    empleados = Empleado.query.all()
    resultado = EmpleadoSchema(many=True).dump(empleados)
    return jsonify(resultado), 200

# Crear un empleado
@api.route('/empleados', methods=['POST'])
@jwt_required()
@admin_required
def crear_empleado():
    datos = request.get_json()
    
    # Validación de datos entrantes
    errors = EmpleadoSchema().validate(datos)
    if errors:
        return jsonify(errors), 400

    role_id = datos.get('role_id')
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Rol no válido"}), 400
    
    nuevo_empleado = Empleado(
        nombre=datos.get('nombre'),
        salario=datos.get('salario'),
        role=role
    )
    
    db.session.add(nuevo_empleado)
    db.session.commit()
    
    return EmpleadoSchema().jsonify(nuevo_empleado), 201

# Editar un empleado
@api.route('/empleados/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    datos = request.get_json()

    # Validación de datos entrantes
    errors = EmpleadoSchema(partial=True).validate(datos)
    if errors:
        return jsonify(errors), 400

    role_id = datos.get('role_id')
    if role_id:
        role = Role.query.get(role_id)
        if not role:
            return jsonify({"error": "Rol no válido"}), 400
        empleado.role = role

    empleado.nombre = datos.get('nombre', empleado.nombre)
    empleado.salario = datos.get('salario', empleado.salario)
    
    db.session.commit()
    
    return EmpleadoSchema().jsonify(empleado), 200

# Eliminar un empleado
@api.route('/empleados/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    
    return jsonify({"message": "Empleado eliminado con éxito"}), 200




