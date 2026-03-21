from flask import Blueprint, request, jsonify
from models import Cita, db
from datetime import datetime

citas_bp = Blueprint('citas', __name__)

# -------- VER HORARIOS --------
@citas_bp.route('/horarios', methods=['GET'])
def ver_horarios():
    citas = Cita.query.all()

    resultado = []
    for c in citas:
        resultado.append({
            "id": c.id,
            "fecha": str(c.fecha),
            "hora": c.hora,
            "estado": c.estado,
            "usuario_id": c.usuario_id
        })

    return jsonify(resultado)


# -------- RESERVAR CITA --------
@citas_bp.route('/reservar', methods=['POST'])
def reservar():
    data = request.json

    usuario_id = data.get("usuario_id")

    if not usuario_id:
        return jsonify({"error": "Usuario no identificado"}), 400

    # 🔥 VALIDAR SI YA TIENE CITA ACTIVA
    ahora = datetime.now().date()

    cita_existente = Cita.query.filter(
        Cita.usuario_id == usuario_id,
        Cita.estado == "reservada",
        Cita.fecha >= ahora
    ).first()

    if cita_existente:
        return jsonify({
            "error": "Ya tienes una cita activa. No puedes reservar otra."
        }), 400

    # 🔥 BUSCAR LA CITA
    cita = Cita.query.filter_by(
        fecha=data['fecha'],
        hora=data['hora']
    ).first()

    if not cita:
        return jsonify({"error": "Cita no existe"}), 404

    if cita.estado != "libre":
        return jsonify({"error": "Horario no disponible"}), 400

    # 🔥 RESERVAR
    cita.estado = "reservada"
    cita.usuario_id = usuario_id

    db.session.commit()

    return jsonify({"msg": "Cita reservada 🔥"})


# -------- CANCELAR CITA --------
@citas_bp.route('/cancelar', methods=['POST'])
def cancelar():
    data = request.json

    cita = Cita.query.filter_by(
        fecha=data['fecha'],
        hora=data['hora']
    ).first()

    if not cita:
        return jsonify({"error": "Cita no existe"}), 404

    cita.estado = "libre"
    cita.usuario_id = None

    db.session.commit()

    return jsonify({"msg": "Cita cancelada"})   

# -------- MIS CITAS --------
@citas_bp.route('/mis_citas/<usuario_id>', methods=['GET'])
def mis_citas(usuario_id):

    citas = Cita.query.filter_by(usuario_id=usuario_id).all()

    resultado = []
    for c in citas:
        resultado.append({
            "id": c.id,
            "fecha": str(c.fecha),
            "hora": c.hora,
            "estado": c.estado
        })

    return jsonify(resultado)