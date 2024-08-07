from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import bp as routes_bp  # Importa el Blueprint desde routes.py
from model import db , Item
from forms import ItemForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

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


@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/item/new', methods=['GET', 'POST'])
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_item.html', form=form)

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', form=form, item=item)

@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)