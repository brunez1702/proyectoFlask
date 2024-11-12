## Proyecto de Gestión de Ventas de Celulares

### Descripción

Este proyecto es una aplicación web desarrollada con Flask que permite gestionar la venta de celulares. La aplicación incluye funcionalidades para manejar equipos, categorías, modelos, ventas, entre otros. Utiliza Flask-SQLAlchemy para la gestión de la base de datos y Flask-Migrate para la creación y aplicación de migraciones.

### Características

- Gestión de equipos (CRUD).
- Gestión de categorías (CRUD).
- Gestión de modelos (CRUD).
- Gestión de stock (CRUD).
- Gestión de empleados (CRUD).
- Gestión de ventas (CRUD).
- Gestión de accesorios (CRUD).
etc...


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

4. Configura la base de datos en el archivo `extensions.py`:

    ```python
    'sqlalchemy.url = %(DATABASE_URL)s
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



### Uso

1. Ejecuta la aplicación:

    ```bash
    flask run
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:5000/` para interactuar con la aplicación.

### Contribución al proyecto:
1. inicializar proyecto: git init
2. configuracion del repositorio remoto: git remote add origin https://github.com/..
3. agregar todos los cambios realizados: git add .
4. creacion del commit con la descripcion realizada: git commit -m "Descripción de los cambios realizados"
5. para subir los cambios realizados a la rama master (ya que estamos trabajando y subiendo los cambios en ella): git push origin master (de lo contrario: git push origin main
)
---> Dato extra: si queres saber la rama en la q estas trabajando: git branch
posibles respuesta:* main o * master
6. Por ultimo pide username(nombre de usuario de Git) y password (la contraseña es un token de accseso personal, hay q generar el token en git).






