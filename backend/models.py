from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    
    fecha_nacimiento = db.Column(db.Date)
    edad = db.Column(db.Integer)
    
    password = db.Column(db.String(200), nullable=False)
    
    rol = db.Column(db.String(10), default="user")  # 👈 IMPORTANTE

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relación con citas
    citas = db.relationship('Cita', backref='usuario', lazy=True)


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    usuario_id = db.Column(
        db.String,
        db.ForeignKey('usuario.id'),  # 👈 RELACIÓN REAL
        nullable=True
    )
    
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    
    estado = db.Column(
        db.String(20),
        default="libre"  # 👈 IMPORTANTE
    )  # libre, reservada, bloqueada

    created_at = db.Column(db.DateTime, default=datetime.utcnow)