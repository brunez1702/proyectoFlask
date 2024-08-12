from flask_sqlalchemy import SQLAlchemy

# Tuve que crear este extentions porque rompia al llamar la base de datos desde los demas archivos
# Con esta 'global' queda mas ordenado importarlo desde los distintos .py
db = SQLAlchemy()
