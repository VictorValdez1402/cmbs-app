from flask import Blueprint, request, jsonify
from models import Usuario, db
from datetime import datetime

# 🔥 JWT
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

CLAVE_ADMIN = "barber123"

# -------- REGISTER --------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    usuario_existente = Usuario.query.filter_by(correo=data['correo']).first()
    if usuario_existente:
        return jsonify({"error": "Correo ya registrado"}), 400

    fecha = datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d")
    edad = datetime.now().year - fecha.year

    rol = data.get("rol", "user")

    if rol == "admin":
        if data.get("clave_admin") != CLAVE_ADMIN:
            return jsonify({"error": "Clave de admin incorrecta"}), 403

    usuario = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo=data['correo'],
        telefono=data['telefono'],
        fecha_nacimiento=fecha,
        edad=edad,
        password=data['password'],
        rol=rol
    )

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado"})


# -------- LOGIN --------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    usuario = Usuario.query.filter_by(correo=data['correo']).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if usuario.password != data['password']:
        return jsonify({"error": "Contraseña incorrecta"}), 401

    # 🔥 TOKEN
    token = create_access_token(identity=usuario.id)

    return jsonify({
        "msg": "Login exitoso",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "rol": usuario.rol
        }
    })