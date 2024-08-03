#Explicacion de como funciona la estructura de cada modelo

class Usuario(db.Model):
#que es: aqui definimos  la clase "usuario". En Flask y SQLAlchemy, una clase que hereda de db.Model representa una tabla en nuestra base de datos.
#Como funciona: db.Model  es la clase base de SQLAlchemy para todos los modelos. Cada clase que hereda de db.Model se convierte en una tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    #que es: esto define una columna en la tabla. La columna se llama "id" y su tipo de dato es "integer" (que siginifa numero entero)
    #como funciona: "primary_key=True" significa que esta columna sera la clave primaria de la tabla. Como sabemos la clave primaria es un identificador unico para cada fila en la tabla. Esto asegura que cada "usuario" tenga un unico "id"
    nombre = db.Column(db.String(50), nullable=False)
    def __repr__(self):
    #que es: define un metodo especial llamado "__repr__". Es una funcion q devuelve una representacion en cadena de texto del objeto "usuario"
    #como funciona: este metodo ayuda a q cuando imprimamos el objeto "usuario" veamos una cadena con el nombre del usuario, el <"usuario juan">
        return f'<Usuario {self.nombre}>'
         #como funciona: este metodo ayuda a q cuando imprimamos el objeto "usuario" veamos una cadena con el nombre del usuario, el <"usuario juan"


#Hagamos de cuenta q tengo una caja de juguetes y quiero mostrarles a mis amigos q hay dentro de la caja
#Entonces vamos a explicar las diferencias q hay entre las etiquetas "__str__" y "__repr__"
#ambos son metodos especiales q se utilizan para definir como se representan los objetos como cadenas de textos.
#"__repr__"= etiqueta de "descripcion tecnica":
    #que es: es como una etiqueta q dice q juguetes y cuantos hay dentro de la caja, entonces podriamos decir q es una descripcion especifica y detalla del objeto
    #proposito: esta disenado para ser mas formal, es util cuando se quiere saber un dato preciso, detallado y para cuando se quiera realizar una depuracion de un objeto
    def __repr__(self):
    return f'<Usuario id={self.id} nombre={self.nombre}>'
    #en esta etiqueta se ve la representacion completa del objeto, es decir todos los detalles q la componen, x eso cuando se llama a "usuario" se pide tmb su id y nombre
    #ej de lo q imprimiria: <Usuario id=1 nombre=Juan>

#"__str__"= etiqueta de "descripcion amigable":
    #que es: es como una etiqueta q dice el nombre del juguete mas te gusta o el q esta en la parte superior de la caja
    #proposito: proporciona una presentacion mas legible y amigable del objeto para el usuario final. Es menos tecnica y mas orientada a la presentacion. Es util cuando se quiere dar una descripcion simple y facil de entender
    def __str__(self):
    return self.nombre
    #esta etiqueta tiene una descripcion simple
    #ej de lo q imprimiria: juan

#ej de ambos:
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario id={self.id} nombre={self.nombre}>'

    def __str__(self):
        return self.nombre

#es util usar ambos para asi tener una representacion detallada y amigable
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#3/8
#QUE ES UN "BLUEPRINT" EN FLASK:

#Un Blueprint es una forma de organizar y agrupar rutas, vistas y otros componentes en una aplicación Flask. Esto ayuda a mantener el código modular y más manejable, especialmente en aplicaciones grandes.
#Cuando usas un Blueprint, estás creando un grupo de rutas que se pueden registrar en la aplicación principal más adelante.
-------------------------------------------------------------------------------------------------------------------------------------------------
# Importar y Registrar Blueprints

from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.categorias import categorias_bp
#Que significa:
#aca estmos importando instancias de "Blueprint" desde los diferentes archivos de rutas que tenemos de cada modelo.
#Los "Blueprints" son una forma de org nuestra app Flak en modulos pequeños y mas entendibles
#Como funciona:
#ej: "usuarios_bp", "productos_bp", etc son instancias de Blueprint que hemos definido en los respectivos archivos (de ruta, son los nombres de los archivos que contienen las rutas de cada modelo) de cada uno (que serian: usuarios.py, productos.py, etc) 
#Entonces decimos que cada Blueprint contiene las RUTAS ESPECIFICAS q estan relacionadas con un tema/funcionalidad en particular de nuestra app.
#Que hay que hacer para que funcione "Blueprint" correctamente:
#en los archivos de nuestras rutas de cada modelo debemos definir y configurar los Blueprints.
#ej de como debe ser cada archivo de ruta de cada modelo:
#routes/usuarios.py:
from flask import Blueprint, render_template

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
def index():
    return "Página de usuarios"
------------------------------------------------------------------------------------------------------
#Como registrar los Blueprints en la Aplicación (app.py):

#En nuestra app principal debmos poner:
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(productos_bp, url_prefix='/productos')
app.register_blueprint(categorias_bp, url_prefix='/categorias')
#Que significan todas estas lineas:
#estas lineas registran cada Blueprint, de cada modelo, en nuestra app Flask
#Como funciona:
#app.register_blueprint(): esto le dice a Flask q incluya en la app cada ruta definida en cada Blueprint
#url_prefix: esto define el prefijo URL q se debe usar en todas las rutas de ese Blueprint. ej: en todas las rutas de "usuarios_bp" estaran definidas por "/usuarios" en la URL
#Ej de como es mas o menos la estructura de mi proyecto:
ProyectoFlask/
│
├── app.py              # Archivo principal de la aplicación
├── model.py           # Definiciones de los modelos
├── routes/             # Directorio para los blueprints
│   ├── __init__.py     # Puede estar vacío, solo para que sea un paquete Python
│   ├── usuarios.py     # Blueprint para usuarios
│   ├── productos.py    # Blueprint para productos
│   └── categorias.py   # Blueprint para categorías
├── config.py           # Configuración de la aplicación
└── ...
#En resumen:

#Modelos: Importas las clases de tus modelos para poder interactuar con la base de datos
#Blueprints: Importas y defines Blueprints para organizar las rutas en tu aplicación.
#Registrar Blueprints: Registras los Blueprints en la aplicación principal para que Flask sepa cómo manejar las rutas.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ARMAMOS LAS RUTAS PARA CADA MODELO:

#codigo de ej:
@bp.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)
-----------------------------------------------------------------------------------
#Definimos la ruta:

@bp.route('/usuarios')
#Que significa esto:
#Este es un decorador de Flask que se usa para asociar una función con una URL específica.
#@app.route('/usuarios'): esto le dice a Flask que cuando un usuario acceda a la URL de "/usuarios", se debe ejecutar la función usuarios(), es decir todo lo que haya dentro.
#Como funciona:
#Flask utiliza este decorador para enrutar las solicitudes HTTP a la función correspondiente.

#POR QUE "BP.ROUTE" Y NO "APP.ROUTE": 
#El uso de @bp.route en lugar de @app.route se debe a la forma en que Flask organiza las rutas cuando se usan Blueprints.
#Por que usar @bp.route:
#bp.route: Este es un decorador específico del Blueprint llamado bp. Se utiliza para definir rutas dentro de ese blueprint. Esto significa que las rutas definidas con @bp.route están asociadas con ese blueprint en particular y no directamente con la aplicación principal (app).
#app.route: Este es el decorador que se usa para definir rutas directamente en la aplicación Flask principal. Se usa cuando no estás utilizando blueprints y deseas definir rutas directamente en el objeto de la aplicación.

#Ej de uso de BLUEPRINTS:
# routes/main.py
from flask import Blueprint, render_template
from models import Usuario, Producto

bp = Blueprint('main', __name__)#bp es un Blueprint que se llama 'main'.

@bp.route('/')#@bp.route('/') define la ruta raíz para este blueprint.
def index():
    return render_template("index.html")

@bp.route('/usuarios')#@bp.route('/usuarios') define una ruta /usuarios para este blueprint.
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)
#RESUMEN:

#@bp.route se usa dentro de un Blueprint para definir rutas específicas a ese blueprint.
#@app.route se usa directamente en la aplicación Flask para definir rutas sin el uso de blueprint
#El uso de blueprints ayuda a organizar tu código, especialmente cuando tienes una aplicación grande con muchas rutas y funcionalidades. Por lo tanto, @bp.route y app.route tienen propósitos diferentes según el contexto en el que estés trabajando.
-----------------------------------------------------------------------------
#Explicamos q hace la "Definición de la Función":

def usuarios():
#Que significa: Esta es la función que se ejecutará cuando alguien acceda a la URL "/usuarios"
#Como funciona: La función "usuarios()"" debe devolver una respuesta que será enviada al navegador del usuario.
#Que hace: En este caso, estás recuperando todos los usuarios y enviándolos a una plantilla.}
------------------------------------------------------------------------------------------------------
#Consulta a la Base de Datos:

usuarios = Usuario.query.all()
#Que significa: "Usuario" es una clase de modelo (esta definida en nuestro modelo "usuario") q esta en la tabla de nuestra base de datos
#Usuario.query.all(): esto recupera todos los registro q hay en la tabla "usuario"
#Como funciona: Usuario.query.all() es una manera de obtener todos los objetos "usuario" que haya registrado en nuestra tabla "usuario" de la base de datos. Esto devuelve una lista de TODOS los usuarios
---------------------------------------------------------------------------------------------------------------------------------------------
#Renderizar la Plantilla:

return render_template('usuarios.html', usuarios=usuarios)
#Que significa: "render_template" es una función de Flask que renderiza una plantilla HTML
#"usuarios.html" es el nombre del archivo de plantilla que se usará para generar la respuesta HTML
#"usuarios=usuarios" pasa los datos (en este caso, la lista de usuarios) a la plantilla para que puedan ser utilizados en la generación del HTML
#Como funciona: Flask buscará el archivo usuarios.html en el directorio de plantillas (por defecto, templates)
#Que debemos hacer: debemos crear el archivo "usuarios.html" en el directorio templates y usa el lenguaje de plantillas Jinja2 para mostrar los datos.

#ej de como seria "usuarios.html"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Usuarios</title>
</head>
<body>
    <h1>Lista de Usuarios</h1>
    <ul>
        {% for usuario in usuarios %} #es un bucle en Jinja2 que itera sobre la lista de usuarios pasada desde la función.
            <li>{{ usuario.nombre }}</li> #muestra el nombre de cada usuario.
        {% endfor %}
    </ul>
</body>
</html>
-----------------------------------------------------------------------------------------------------------------------------------------
#Ej de ruta y de html para el modelo Productos:
#RUTA
@app.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)
#HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Productos</title>
</head>
<body>
    <h1>Lista de Productos</h1>
    <ul>
        {% for producto in productos %}
            <li>{{ producto.nombre }} - ${{ producto.precio }}</li>
        {% endfor %}
    </ul>
</body>
</html>
--------------------------------------------------------------------------------------
#Ej para Categorias:
#RUTA
@app.route('/categorias')
def categorias():
    categorias = CategoriaProducto.query.all()
    return render_template('categorias.html', categorias=categorias)
#HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Categorías</title>
</head>
<body>
    <h1>Lista de Categorías</h1>
    <ul>
        {% for categoria in categorias %}
            <li>{{ categoria.nombre }}</li>
        {% endfor %}
    </ul>
</body>
</html>
#EN RESUMEN:

#Definición de Ruta: Usa @app.route para asociar una URL con una función.
#Función de Ruta: Define qué hacer cuando se accede a esa URL, como consultar la base de datos.
#Consulta a la Base de Datos: Usa el modelo para obtener datos
#Renderizar Plantilla: Usa render_template para enviar los datos a una plantilla HTML y generar la respuesta que el usuario verá.
-------------------------------------------------------------------------------------------------------------------------------------------
#LOS HTML DE CADA MODELO DEBE IR EN EL ARCHIVO DE LOS TEMPLATES!!!
#Por q: Esto permite que Flask pueda encontrar y renderizar las plantillas HTML cuando se hace una solicitud a la aplicación web.
#Ej de como debe quedar todo:
my_flask_app/
├── app.py
├── models.py
├── routes/
│   ├── usuarios.py
│   ├── productos.py
│   └── categorias.py
├── templates/
│   ├── usuarios.html
│   ├── productos.html
│   ├── categorias.html
│   └── base.html
└── static/
    └── (archivos estáticos como CSS, JS, imágenes, etc.)
#Dentro de templates, crea archivos HTML con nombres que reflejen el propósito de la plantilla

#RESUMEN:
#Coloca todos los archivos HTML en el directorio templates para que Flask pueda encontrarlos y renderizarlos.
#Usa nombres descriptivos para los archivos HTML para que sea claro qué plantilla corresponde a qué vista.



















