import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
from routes.admin import admin_bp

# 🔥 NUEVO
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from models import Cita

load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 JWT
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# DB
uri = os.getenv("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# IMPORTAR RUTAS
from routes.auth import auth_bp
from routes.citas import citas_bp  

# REGISTRAR RUTAS
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(citas_bp, url_prefix='/citas') 
app.register_blueprint(admin_bp, url_prefix='/admin') 

@app.route('/')
def home():
    return jsonify({"message": "CM Reservas - Backend funcionando"})

# 🔔 RECORDATORIOS AUTOMÁTICOS
def verificar_citas():
    with app.app_context():
        ahora = datetime.now()
        en_20_min = ahora + timedelta(minutes=20)

        citas = Cita.query.filter_by(estado="reservada").all()

        for c in citas:
            try:
                fecha_hora = datetime.strptime(f"{c.fecha} {c.hora}", "%Y-%m-%d %H:%M")

                if ahora < fecha_hora <= en_20_min:
                    print(f"🔔 Recordatorio: cita en 20 min para usuario {c.usuario_id}")

                    # 🔥 AQUÍ luego conectamos WhatsApp

            except:
                pass

# 🔥 INICIAR SCHEDULER
scheduler = BackgroundScheduler()
scheduler.add_job(verificar_citas, 'interval', minutes=1)
scheduler.start()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)