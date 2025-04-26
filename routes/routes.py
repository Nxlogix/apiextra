from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from controllers.controllers import (
    create_usuario,
    create_producto,
    create_categoria,
    buscar_productos_por_categoria,
    buscar_productos_por_nombre
)
from models.models import Usuario, Producto, Categoria

# Blueprints
usuario_bp = Blueprint('usuarios', __name__)
productos_bp = Blueprint('productos', __name__)

# Rutas de Usuarios
@usuario_bp.route('/', methods=['POST'])
def user_store():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Usuarios
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - nombre
              - password
            properties:
              email:
                type: string
                example: usuario@example.com
              nombre:
                type: string
                example: Usuario Prueba
              password:
                type: string
                example: password123
    responses:
      201:
        description: Usuario creado exitosamente
      400:
        description: Faltan campos en la solicitud
    """
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    password = data.get('password')

    if not all([email, nombre, password]):
        return jsonify({"error": "Rellena todos los campos por favor"}), 400
    
    return create_usuario(nombre, email, password)


@usuario_bp.route('/login', methods=['POST'])
def login_usuario_route():
    """
    Iniciar sesión con un usuario existente
    ---
    tags:
      - Usuarios
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
                example: usuario@example.com
              password:
                type: string
                example: password123
    responses:
      200:
        description: Inicio de sesión exitoso
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: jwt_token_example
                usuario:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    nombre:
                      type: string
                      example: Usuario Prueba
                    email:
                      type: string
                      example: usuario@example.com
      400:
        description: El email y la contraseña son requeridos
      401:
        description: Credenciales inválidas
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"msg": "El email y la contraseña son requeridos"}), 400

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
            }), 200
        else:
            return jsonify({"msg": "Credenciales inválidas. Revisa el email o la contraseña."}), 401
    except Exception as e:
        print(f"ERROR durante el inicio de sesión: {e}")
        return jsonify({'msg': 'Ocurrió un error durante el inicio de sesión.'}), 500


# Rutas de Categorías
@productos_bp.route('/categorias', methods=['POST'])
def categoria_store():
    """
    Crear una nueva categoría
    ---
    tags:
      - Categorías
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - nombre
            properties:
              nombre:
                type: string
                example: Electrónica
              descripcion:
                type: string
                example: Artículos tecnológicos y electrónicos
    responses:
      201:
        description: Categoría creada exitosamente
      400:
        description: El nombre de la categoría es obligatorio
    """
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    if not nombre:
        return jsonify({"error": "El nombre de la categoría es obligatorio"}), 400
    
    return create_categoria(nombre, descripcion)


@productos_bp.route('/categorias', methods=['GET'])
def get_categorias():
    """
    Obtener lista de categorías
    ---
    tags:
      - Categorías
    responses:
      200:
        description: Lista de categorías obtenida exitosamente
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  nombre:
                    type: string
                    example: Electrónica
                  descripcion:
                    type: string
                    example: Artículos tecnológicos y electrónicos
      404:
        description: No hay categorías disponibles
    """
    try:
        categorias = Categoria.query.all()
        if not categorias:
            return jsonify({"msg": "No hay categorías disponibles"}), 404
        return jsonify([categoria.to_dict() for categoria in categorias]), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener categorías'}), 500


# Rutas de Productos
@productos_bp.route('/productos', methods=['POST'])
def producto_store():
    """
    Crear un nuevo producto asociado a una categoría existente
    ---
    tags:
      - Productos
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - nombre
              - precio
              - cantidad
              - categoria_id
            properties:
              nombre:
                type: string
                example: Laptop
              precio:
                type: float
                example: 999.99
              cantidad:
                type: integer
                example: 10
              categoria_id:
                type: integer
                example: 1
    responses:
      201:
        description: Producto creado exitosamente
      400:
        description: Faltan campos requeridos
    """
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')
    cantidad = data.get('cantidad')
    categoria_id = data.get('categoria_id')

    if not all([nombre, precio, cantidad, categoria_id]):
        return jsonify({"error": "Todos los campos son requeridos"}), 400
    
    return create_producto(nombre, precio, cantidad, categoria_id)


@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    """
    Obtener lista de productos
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos obtenida exitosamente
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  nombre:
                    type: string
                    example: Laptop
                  precio:
                    type: float
                    example: 999.99
                  cantidad:
                    type: integer
                    example: 10
                  categoria:
                    type: object
                    properties:
                      nombre:
                        type: string
                        example: Electrónica
      500:
        description: Error al obtener productos
    """
    try:
        productos = Producto.query.all()
        return jsonify([producto.to_dict() for producto in productos]), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener productos'}), 500