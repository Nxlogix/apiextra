from config import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email
        }

# Modelo de Categoría
class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

# Modelo de Producto
class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

    def __init__(self, nombre, precio, cantidad, categoria_id):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria_id = categoria_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "categoria": self.categoria.to_dict() if self.categoria else None
        }