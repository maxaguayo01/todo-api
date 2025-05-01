from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from config import Config
from model import db  # Aquí importamos db desde model.py
from tasks import task_bp  # Importamos el blueprint 'task_bp' desde tasks.py
from scheduler import start_scheduler

# Cargar variables de .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
JWTManager(app)

# Registrar el blueprint de tareas (tasks)
app.register_blueprint(task_bp)

# Crear tablas y arrancar el scheduler
with app.app_context():
    db.create_all()
    start_scheduler()

# Ruta de salud (para comprobar que la API está funcionando)
@app.route('/')
def index():
    return {'msg': 'API funcionando correctamente'}, 200

if __name__ == '__main__':
    app.run(debug=True)
