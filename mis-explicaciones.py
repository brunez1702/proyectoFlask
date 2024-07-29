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