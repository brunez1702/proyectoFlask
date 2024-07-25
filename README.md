## Proyecto de Gestión de Ventas de Celulares

### Descripción

Este proyecto es una aplicación web desarrollada con Flask que permite gestionar la venta de celulares. La aplicación incluye funcionalidades para manejar equipos, categorías, modelos y costos, entre otros. Utiliza Flask-SQLAlchemy para la gestión de la base de datos y Flask-Migrate para la creación y aplicación de migraciones.

### Características

- Gestión de equipos (CRUD).
- Gestión de categorías (CRUD).
- Gestión de modelos (CRUD).
- Gestión de costos (CRUD).

### Requisitos

- Python 3.7 o superior
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

### Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura la base de datos en el archivo `config.py`:

    ```python
    SQLALCHEMY_DATABASE_URI = 'sqlite:///celulares.db'
    ```

### Migraciones

1. Inicializa las migraciones:

    ```bash
    flask db init
    ```

2. Genera una migración inicial:

    ```bash
    flask db migrate -m "Initial migration"
    ```

3. Aplica la migración a la base de datos:

    ```bash
    flask db upgrade
    ```

### Estructura del Proyecto

```plaintext
.
├── app.py
├── config.py
├── forms.py
├── models.py
├── requirements.txt
├── templates
│   ├── base.html
│   ├── index.html
│   ├── equipos
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── list.html
│   │   └── show.html
│   ├── categorias
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── list.html
│   │   └── show.html
│   ├── modelos
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── list.html
│   │   └── show.html
│   └── costos
│       ├── create.html
│       ├── edit.html
│       ├── list.html
│       └── show.html
└── venv
```

### Archivos Clave

#### app.py

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import EquipoForm, CategoriaForm, ModeloForm, CostoForm

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Equipo, Categoria, Modelo, Costo

@app.route('/')
def index():
    return render_template('index.html')

# Rutas CRUD para equipos, categorías, modelos y costos

if __name__ == '__main__':
    app.run(debug=True)
```

#### config.py

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'celulares.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'
```

#### models.py

```python
from app import db

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    costo_id = db.Column(db.Integer, db.ForeignKey('costo.id'), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Costo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
```

#### forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EquipoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    costo_id = SelectField('Costo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class ModeloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class CostoForm(FlaskForm):
    valor = FloatField('Valor', validators=[DataRequired()])
    submit = SubmitField('Guardar')
```

### Uso

1. Ejecuta la aplicación:

    ```bash
    flask run
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:5000/` para interactuar con la aplicación.

### Contribución

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva_caracteristica`).
3. Haz tus cambios y haz commit (`git commit -am 'Agrega nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva_caracteristica`).
5. Crea un nuevo Pull Request.

### Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
