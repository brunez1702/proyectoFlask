from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from extensions import db, jwt # Importar db desde extensions.py
from routes import bp  # Importar el Blueprint desde routes.py
from model import init_roles, Usuario
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'q_miras'

    # Inicializar SQLAlchemy, Migrate y jwt con la app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Registrar el blueprint de rutas
    app.register_blueprint(bp)  # Registra el blueprint desde routes.py

      # Llamar a init_roles() después de inicializar la base de datos
    with app.app_context():
        init_roles() 

    # Función para cargar el usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))  # Devuelve el usuario con el ID dado


    @app.route('/')
    def index():
        items = Item.query.all() 
        return render_template('index.html', items=items)

    return app

# Ejecución de la Aplicación
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


