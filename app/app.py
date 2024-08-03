from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import bp as routes_bp  # Importa el Blueprint desde routes.py
from model import db 

# Crear instancias globales de SQLAlchemy y Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy y Migrate con la app
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar el blueprint de rutas
    app.register_blueprint(routes_bp)  # Registra el blueprint desde routes.py

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# Ejecución de la Aplicación
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
