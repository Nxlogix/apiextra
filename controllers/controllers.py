from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Usuario, Categoria, Producto  # Asegúrate de importar los modelos necesarios

# Controlador: Crear Usuario
def create_usuario(nombre, email, password):
    try:
        nuevo_usuario = Usuario(nombre, email, password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el nuevo usuario'}), 500

# Controlador: Login de Usuario
def login_usuario(email, password):
    try:
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            access_token = create_access_token(identity=usuario.id)
            return jsonify({
                'access_token': access_token,
                'usuario': {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email
                }
            })
        return jsonify({"msg": "Datos incorrectos"}), 401
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error en el inicio de sesión'}), 500

# Controlador: Crear Producto
def create_producto(nombre, precio, cantidad, categoria_id):
    try:
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({'msg': 'La categoría no existe'}), 404
        
        nuevo_producto = Producto(nombre, precio, cantidad, categoria_id)
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify(nuevo_producto.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el producto'}), 500

# Controlador: Crear Categoría
def create_categoria(nombre, descripcion=None):
    try:
        nueva_categoria = Categoria(nombre, descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        return jsonify(nueva_categoria.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear la categoría'}), 500

# Controlador: Buscar Productos por Categoría
def buscar_productos_por_categoria(categoria_nombre):
    try:
        categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
        if not categoria:
            return jsonify({'msg': 'No se encontró la categoría'}), 404
        
        productos = Producto.query.filter_by(categoria_id=categoria.id).all()
        return jsonify([producto.to_dict() for producto in productos]), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al buscar productos por categoría'}), 500

# Controlador: Buscar Productos por Nombre
def buscar_productos_por_nombre(nombre_producto):
    try:
        productos = Producto.query.filter(Producto.nombre.ilike(f"%{nombre_producto}%")).all()
        if not productos:
            return jsonify({'msg': 'No se encontraron productos con ese nombre'}), 404
        
        return jsonify([producto.to_dict() for producto in productos]), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al buscar productos por nombre'}), 500
    
    
    
# Controlador: Editar Usuario
def edit_usuario(usuario_id, nombre=None, email=None, password=None):
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'msg': 'El usuario no existe'}), 404
        
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        if password:
            usuario.password = generate_password_hash(password)

        db.session.commit()
        return jsonify({'msg': 'Usuario actualizado con éxito', 'usuario': usuario.to_dict()}), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al editar el usuario'}), 500
    
    # Controlador: Eliminar Usuario
def delete_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'msg': 'El usuario no existe'}), 404
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'msg': 'Usuario eliminado con éxito'}), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al eliminar el usuario'}), 500
    
# Controlador: Editar Producto
def edit_producto(producto_id, nombre=None, precio=None, cantidad=None, categoria_id=None):
    try:
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'msg': 'El producto no existe'}), 404

        if nombre:
            producto.nombre = nombre
        if precio:
            producto.precio = precio
        if cantidad:
            producto.cantidad = cantidad
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                return jsonify({'msg': 'La categoría especificada no existe'}), 404
            producto.categoria_id = categoria_id

        db.session.commit()
        return jsonify({'msg': 'Producto actualizado con éxito', 'producto': producto.to_dict()}), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al editar el producto'}), 500
# Controlador: Eliminar Producto
def delete_producto(producto_id):
    try:
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'msg': 'El producto no existe'}), 404
        
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'msg': 'Producto eliminado con éxito'}), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al eliminar el producto'}), 500
