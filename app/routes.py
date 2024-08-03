from flask import Blueprint, render_template
from model import Usuario, Producto, CategoriaProducto, Marca, Fabricante, Modelo, Caracteristica, Equipo, Stock, Proveedor, Accesorio, Empleado

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
    return render_template('usuarios.html', usuarios=usuarios)

@bp.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@bp.route('/categorias')
def categorias():
    categorias = CategoriaProducto.query.all()
    return render_template('categorias.html', categorias=categorias)

@bp.route('/marcas')
def marcas():
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)

@bp.route('/fabricantes')
def fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@bp.route('/modelos')
def modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

@bp.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@bp.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('equipos.html', equipos=equipos)

@bp.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

@bp.route('/proveedores')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@bp.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

@bp.route('/empleados')
def empleados():
    empleados = Empleado.query.all()
    return render_template('empleados.html', empleados=empleados)
