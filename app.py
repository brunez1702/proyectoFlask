from flask import Flask, render_template
from flask_migrate import Migrate
from extensions import db  # Importar db desde extensions.py
from routes import bp as routes_bp  # Importar el Blueprint desde routes.py

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy y Migrate con la app
    db.init_app(app)
    migrate = Migrate(app, db)

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