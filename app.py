from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from extensions import db, jwt # Importar db desde extensions.py
from routes import bp  # Importar el Blueprint desde routes.py


def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'

    # Inicializar SQLAlchemy, Migrate y jwt con la app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    # Registrar el blueprint de rutas
    app.register_blueprint(bp)  # Registra el blueprint desde routes.py


    @app.route('/')
    def index():
        items = Item.query.all() 
        return render_template('index.html', items=items)

    return app

# Ejecución de la Aplicación
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


