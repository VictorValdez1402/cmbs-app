from flask import Blueprint, request, jsonify
from models import Cita, db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Crear horarios del día
@admin_bp.route('/crear_horarios', methods=['POST'])
def crear_horarios():
    data = request.json

    fecha = datetime.strptime(data['fecha'], "%Y-%m-%d")

    horas = [
        "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00"
    ]

    for hora in horas:
        existe = Cita.query.filter_by(fecha=fecha, hora=hora).first()

        if not existe:
            nueva = Cita(
                fecha=fecha,
                hora=hora,
                estado="libre"
            )
            db.session.add(nueva)

    db.session.commit()

    return jsonify({"msg": "Horarios creados"})