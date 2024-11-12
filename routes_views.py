from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from extensions import db
from model import   Usuario, Producto, CategoriaProducto, Marca, Fabricante, Modelo, Caracteristica, Equipo, Stock, Proveedor, Accesorio, Empleado, Venta, Item, User, Role
from schemas import UsuarioSchema, ProductoSchema
from flask_jwt_extended import  jwt_required, get_jwt_identity, create_access_token
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from datetime import timedelta

# Crear un Blueprint
bp = Blueprint('main', __name__)

# Función para verificar si el usuario es Admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()  # Obtenemos la identidad del JWT
        user = User.query.filter_by(username=current_user).first()
        if user and user.role == 'Admin':
            return fn(*args, **kwargs)
        else:
            return jsonify({"message": "Acceso no autorizado"}), 403
    return wrapper

# Endpoint para obtener todos los objetos de Item (sin restricción)
@bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    result = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
    return jsonify(result)

# Endpoint para crear un objeto nuevo (solo Admin)
@bp.route('/items', methods=['POST'])
@jwt_required()
@admin_required  # Solo accesible por Admin
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Objeto creado exitosamente"}), 201



# Ruta para la página principal
@bp.route('/')
def index():
    return render_template("index.html")

 #registro
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = generate_password_hash(password, method='sha256')

        # Crear nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado exitosamente!', 'success')
        return redirect(url_for('login'))  # Redirigir a login después del registro

    return render_template('register.html')  # Formulario de registro


 #iniciar sesion con Flask-Login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar al usuario por el email
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)  # Iniciar sesión con Flask-Login
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('dashboard'))  # Redirigir a la página de inicio o dashboard

        flash('Credenciales incorrectas', 'danger')  # Mensaje si las credenciales son incorrectas

    return render_template('login.html')  # Formulario de login

#cerrar sesion
@bp.route('/logout')
def logout():
    logout_user()  # Cerrar sesión con Flask-Login
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))  # Redirigir a la página de login después de cerrar sesión


# iniciar sesion para autenticación con JWT (para APIs)
@bp.route('/login-api', methods=['POST'])
def login_api():
    data = request.get_json()  # Recibe datos JSON
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

# Rutas para Usuarios
@bp.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('subitem/usuarios.html', usuarios=usuarios)

@bp.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('nombre')
    if nombre:
        nuevo_usuario = Usuario(nombre=nombre)
        db.session.add(nuevo_usuario)
        db.session.commit()
    return redirect(url_for('main.usuarios'))

@bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('main.usuarios'))
    return render_template('subitem/editar_usuario.html', usuario=usuario)

@bp.route('/usuarios/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('main.usuarios'))

@bp.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('subitem/productos.html', productos=productos)


@bp.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        categoria_id = request.form['categoria_id']
        nuevo_producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad, categoria_id=categoria_id)
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado con éxito', 'success')
        return redirect(url_for('lista_productos'))
    categorias = CategoriaProducto.query.all()
    return render_template('crear_producto.html', categorias=categorias)

@bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.cantidad = request.form['cantidad']
        producto.categoria_id = request.form['categoria_id']
        db.session.commit()
        flash('Producto actualizado con éxito', 'success')
        return redirect(url_for('lista_productos'))
    categorias = CategoriaProducto.query.all()
    return render_template('editar_producto.html', producto=producto, categorias=categorias)

@bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('lista_productos'))

# Rutas para Categorías de Productos
@bp.route('/categorias')
def lista_categorias():
    categorias = CategoriaProducto.query.all()
    return render_template('categorias.html', categorias=categorias)


@bp.route('/categorias/crear', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        nueva_categoria = CategoriaProducto(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        flash('Categoría creada con éxito', 'success')
        return redirect(url_for('categorias.lista_categorias'))
    return render_template('crear_categoria.html')

@bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form['descripcion']
        db.session.commit()
        flash('Categoría actualizada con éxito', 'success')
        return redirect(url_for('categorias.lista_categorias'))
    return render_template('editar_categoria.html', categoria=categoria)

@bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada con éxito', 'success')
    return redirect(url_for('categorias.lista_categorias'))

# Rutas para Ventas
@bp.route('/ventas')
def lista_ventas():
    ventas = Venta.query.all()
    return render_template('ventas.html', ventas=ventas)

@bp.route('/ventas/crear', methods=['GET', 'POST'])
def crear_venta():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']
        nueva_venta = Venta(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta creada con éxito', 'success')
        return redirect(url_for('lista_ventas'))
    usuarios = Usuario.query.all()
    productos = Producto.query.all()
    return render_template('crear_venta.html', usuarios=usuarios, productos=productos)

@bp.route('/ventas/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    if request.method == 'POST':
        venta.usuario_id = request.form['usuario_id']
        venta.producto_id = request.form['producto_id']
        venta.cantidad = request.form['cantidad']
        db.session.commit()
        flash('Venta actualizada con éxito', 'success')
        return redirect(url_for('lista_ventas'))
    usuarios = Usuario.query.all()
    productos = Producto.query.all()
    return render_template('editar_venta.html', venta=venta, usuarios=usuarios, productos=productos)

@bp.route('/ventas/eliminar/<int:id>', methods=['POST'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada con éxito', 'success')
    return redirect(url_for('lista_ventas'))


# Rutas para Marcas
@bp.route('/marcas')
def lista_marcas():
    marcas = Marca.query.all()
    return render_template('subitem/marcas.html', marcas=marcas)

@bp.route('/marcas/crear', methods=['GET', 'POST'])
def crear_marca():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        flash('Marca creada con éxito', 'success')
        return redirect(url_for('lista_marcas'))
    return render_template('crear_marca.html')

@bp.route('/marcas/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        flash('Marca actualizada con éxito', 'success')
        return redirect(url_for('lista_marcas'))
    return render_template('editar_marca.html', marca=marca)

@bp.route('/marcas/eliminar/<int:id>', methods=['POST'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marca eliminada con éxito', 'success')
    return redirect(url_for('lista_marcas'))

# Rutas para Fabricantes
@bp.route('/fabricantes')
def lista_fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)


@bp.route('/fabricantes/crear', methods=['GET', 'POST'])
def crear_fabricante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        pais_origen = request.form['pais_origen']
        nuevo_fabricante = Fabricante(nombre=nombre, pais_origen=pais_origen)
        db.session.add(nuevo_fabricante)
        db.session.commit()
        flash('Fabricante creado con éxito', 'success')
        return redirect(url_for('lista_fabricantes'))
    return render_template('crear_fabricante.html')


@bp.route('/fabricantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    if request.method == 'POST':
        fabricante.nombre = request.form['nombre']
        fabricante.pais_origen = request.form['pais_origen']
        db.session.commit()
        flash('Fabricante actualizado con éxito', 'success')
        return redirect(url_for('lista_fabricantes'))
    return render_template('editar_fabricante.html', fabricante=fabricante)

@bp.route('/fabricantes/eliminar/<int:id>', methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    flash('Fabricante eliminado con éxito', 'success')
    return redirect(url_for('lista_fabricantes'))

# Rutas para Modelos
@bp.route('/modelos')
def lista_modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)


@bp.route('/modelos/crear', methods=['GET', 'POST'])
def crear_modelo():
    if request.method == 'POST':
        nombre_modelo = request.form['nombre_modelo']
        fabricante_id = request.form['fabricante_id']
        marca_id = request.form['marca_id']
        nuevo_modelo = Modelo(nombre_modelo=nombre_modelo, fabricante_id=fabricante_id, marca_id=marca_id)
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash('Modelo creado con éxito', 'success')
        return redirect(url_for('lista_modelos'))
    fabricantes = Fabricante.query.all()
    marcas = Marca.query.all()
    return render_template('crear_modelo.html', fabricantes=fabricantes, marcas=marcas)


@bp.route('/modelos/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    if request.method == 'POST':
        modelo.nombre_modelo = request.form['nombre_modelo']
        modelo.fabricante_id = request.form['fabricante_id']
        modelo.marca_id = request.form['marca_id']
        db.session.commit()
        flash('Modelo actualizado con éxito', 'success')
        return redirect(url_for('lista_modelos'))
    fabricantes = Fabricante.query.all()
    marcas = Marca.query.all()
    return render_template('editar_modelo.html', modelo=modelo, fabricantes=fabricantes, marcas=marcas)

@bp.route('/modelos/eliminar/<int:id>', methods=['POST'])
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    flash('Modelo eliminado con éxito', 'success')
    return redirect(url_for('lista_modelos'))

# Rutas para Características
@bp.route('/caracteristicas')
def lista_caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)


@bp.route('/caracteristicas/crear', methods=['GET', 'POST'])
def crear_caracteristica():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        modelo_id = request.form['modelo_id']
        nueva_caracteristica = Caracteristica(tipo=tipo, descripcion=descripcion, modelo_id=modelo_id)
        db.session.add(nueva_caracteristica)
        db.session.commit()
        flash('Característica creada con éxito', 'success')
        return redirect(url_for('lista_caracteristicas'))
    modelos = Modelo.query.all()
    return render_template('crear_caracteristica.html', modelos=modelos)


@bp.route('/caracteristicas/editar/<int:id>', methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    if request.method == 'POST':
        caracteristica.tipo = request.form['tipo']
        caracteristica.descripcion = request.form['descripcion']
        caracteristica.modelo_id = request.form['modelo_id']
        db.session.commit()
        flash('Característica actualizada con éxito', 'success')
        return redirect(url_for('lista_caracteristicas'))
    modelos = Modelo.query.all()
    return render_template('editar_caracteristica.html', caracteristica=caracteristica, modelos=modelos)

@bp.route('/caracteristicas/eliminar/<int:id>', methods=['POST'])
def eliminar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    flash('Característica eliminada con éxito', 'success')
    return redirect(url_for('lista_caracteristicas'))

# Rutas para Equipos
@bp.route('/equipos')
def lista_equipos():
    equipos = Equipo.query.all()
    return render_template('subitem/equipos.html', equipos=equipos)

@bp.route('/equipos/crear', methods=['GET', 'POST'])
def crear_equipo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        modelo_id = request.form['modelo_id']
        costo = request.form['costo']
        stock = request.form['stock']
        nuevo_equipo = Equipo(nombre=nombre, modelo_id=modelo_id, costo=costo, stock=stock)
        db.session.add(nuevo_equipo)
        db.session.commit()
        flash('Equipo creado con éxito', 'success')
        return redirect(url_for('lista_equipos'))
    modelos = Modelo.query.all()
    return render_template('crear_equipo.html', modelos=modelos)

@bp.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.modelo_id = request.form['modelo_id']
        equipo.costo = request.form['costo']
        equipo.stock = request.form['stock']
        db.session.commit()
        flash('Equipo actualizado con éxito', 'success')
        return redirect(url_for('lista_equipos'))
    modelos = Modelo.query.all()
    return render_template('editar_equipo.html', equipo=equipo, modelos=modelos)

@bp.route('/equipos/eliminar/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado con éxito', 'success')
    return redirect(url_for('lista_equipos'))

# Rutas para Stocks
@bp.route('/stocks')
def lista_stocks():
    stocks = Stock.query.all()
    return render_template('subitem/stocks.html', stocks=stocks)

@bp.route('/stocks/crear', methods=['GET', 'POST'])
def crear_stock():
    if request.method == 'POST':
        equipo_id = request.form['equipo_id']
        cantidad_disponible = request.form['cantidad_disponible']
        ubicacion_almacen = request.form['ubicacion_almacen']
        nuevo_stock = Stock(equipo_id=equipo_id, cantidad_disponible=cantidad_disponible, ubicacion_almacen=ubicacion_almacen)
        db.session.add(nuevo_stock)
        db.session.commit()
        flash('Stock creado con éxito', 'success')
        return redirect(url_for('lista_stocks'))
    equipos = Equipo.query.all()
    return render_template('crear_stock.html', equipos=equipos)

@bp.route('/stocks/editar/<int:id>', methods=['GET', 'POST'])
def editar_stock(id):
    stock = Stock.query.get_or_404(id)
    if request.method == 'POST':
        stock.equipo_id = request.form['equipo_id']
        stock.cantidad_disponible = request.form['cantidad_disponible']
        stock.ubicacion_almacen = request.form['ubicacion_almacen']
        db.session.commit()
        flash('Stock actualizado con éxito', 'success')
        return redirect(url_for('lista_stocks'))
    equipos = Equipo.query.all()
    return render_template('editar_stock.html', stock=stock, equipos=equipos)

@bp.route('/stocks/eliminar/<int:id>', methods=['POST'])
def eliminar_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock eliminado con éxito', 'success')
    return redirect(url_for('lista_stocks'))


# Rutas para Accesorios
@bp.route('/accesorios')
def lista_accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)


@bp.route('/accesorios/crear', methods=['GET', 'POST'])
def crear_accesorio():
    if request.method == 'POST':
        tipo = request.form['tipo']
        compatible_con = request.form['compatible_con']
        nuevo_accesorio = Accesorio(tipo=tipo, compatible_con=compatible_con)
        db.session.add(nuevo_accesorio)
        db.session.commit()
        flash('Accesorio creado con éxito', 'success')
        return redirect(url_for('lista_accesorios'))
    return render_template('crear_accesorio.html')

@bp.route('/accesorios/editar/<int:id>', methods=['GET', 'POST'])
def editar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    if request.method == 'POST':
        accesorio.tipo = request.form['tipo']
        accesorio.compatible_con = request.form['compatible_con']
        db.session.commit()
        flash('Accesorio actualizado con éxito', 'success')
        return redirect(url_for('lista_accesorios'))
    return render_template('editar_accesorio.html', accesorio=accesorio)


@bp.route('/accesorios/eliminar/<int:id>', methods=['POST'])
def eliminar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    db.session.delete(accesorio)
    db.session.commit()
    flash('Accesorio eliminado con éxito', 'success')
    return redirect(url_for('lista_accesorios'))

# Rutas para Empleados
@bp.route('/empleados')
def lista_empleados():
    empleados = Empleado.query.all()
    return render_template('empleados.html', empleados=empleados)

@bp.route('/empleados/crear', methods=['GET', 'POST'])
def crear_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        puesto = request.form['role_id']  # Esto obtendrá el ID del rol seleccionado
        
        # Buscar el rol por ID (ya que el formulario enviará el ID del rol)
        role = Role.query.get(puesto)
        
        if not role:
            flash('Rol no válido', 'danger')
            return redirect(url_for('main.crear_empleado'))  # Asegúrate de tener este nombre de ruta

        # Crear el nuevo empleado con el rol seleccionado
        nuevo_empleado = User(username=nombre, role=role)
        db.session.add(nuevo_empleado)
        db.session.commit()
        flash('Empleado creado con éxito', 'success')
        return redirect(url_for('main.lista_empleados'))  # Asegúrate de tener esta ruta también
    
    # Obtener todos los roles disponibles para pasarlos al formulario
    roles = Role.query.all()
    return render_template('crear_empleado.html', roles=roles)


@bp.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    empleado = User.query.get_or_404(id)
    
    if request.method == 'POST':
        empleado.username = request.form['nombre']
        puesto = request.form['role_id']  # Esto obtendrá el ID del rol seleccionado
        
        # Buscar el rol por ID (ya que el formulario enviará el ID del rol)
        role = Role.query.get(puesto)
        
        if not role:
            flash('Rol no válido', 'danger')
            return redirect(url_for('main.editar_empleado', id=empleado.id))  # Asegúrate de tener este nombre de ruta

        # Actualizar el rol del empleado
        empleado.role = role
        db.session.commit()
        flash('Empleado actualizado con éxito', 'success')
        return redirect(url_for('main.lista_empleados'))  # Asegúrate de tener esta ruta también
    
    # Obtener todos los roles disponibles para pasarlos al formulario
    roles = Role.query.all()
    return render_template('editar_empleado.html', empleado=empleado, roles=roles)


@bp.route('/empleados/eliminar/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    flash('Empleado eliminado con éxito', 'success')
    return redirect(url_for('lista_empleados'))
