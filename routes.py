from flask import Blueprint, render_template, request, redirect, url_for
from model import db, Usuario, Producto, CategoriaProducto, Marca, Fabricante, Modelo, Caracteristica, Equipo, Stock, Proveedor, Accesorio, Empleado

# Crear un Blueprint
bp = Blueprint('main', __name__)

# Ruta para la página principal
@bp.route('/')
def index():
    return render_template("index.html")

# Rutas para cada modelo
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

@bp.route('/categorias')
def categorias():
    categorias = CategoriaProducto.query.all()
    return render_template('subitem/categorias.html', categorias=categorias)

@bp.route('/marcas')
def marcas():
    marcas = Marca.query.all()
    return render_template('subitem/marcas.html', marcas=marcas)

@bp.route('/fabricantes')
def fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('subitem/fabricantes.html', fabricantes=fabricantes)

@bp.route('/modelos')
def modelos():
    modelos = Modelo.query.all()
    return render_template('subitem/modelos.html', modelos=modelos)

@bp.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('subitem/caracteristicas.html', caracteristicas=caracteristicas)

@bp.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('subitem/equipos.html', equipos=equipos)

@bp.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('subitem/stocks.html', stocks=stocks)

@bp.route('/proveedores')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('subitem/proveedores.html', proveedores=proveedores)

@bp.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.all()
    return render_template('subitem/accesorios.html', accesorios=accesorios)

@bp.route('/empleados')
def empleados():
    empleados = Empleado.query.all()
    return render_template('subitem/empleados.html', empleados=empleados)
