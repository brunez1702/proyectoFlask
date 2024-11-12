from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Tuve que crear este extentions porque rompia al llamar la base de datos desde los demas archivos
# Con esta 'global' queda mas ordenado importarlo desde los distintos .py
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
