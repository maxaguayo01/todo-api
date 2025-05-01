# todo-api
technical test for dinametra
To-Do API – Prueba Técnica Dinametra
API RESTful para gestionar tareas de usuarios con autenticación JWT, manejo de base de datos SQL y eliminación automática de tareas completadas cada 10 minutos.
Tecnologías utilizadas
- Python 3
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- APScheduler
- SQLite
- Postman (para pruebas)
Estructura del Proyecto
prueba_dinametra/
├── app.py               # Archivo principal que ejecuta la app
├── config.py            # Configuración de Flask y DB
├── model.py             # Modelos: User y Task
├── tasks.py             # Contiene todos los endpoints (registro, login, tareas)
├── scheduler.py         # Limpieza automática de tareas completadas
├── .env                 # Variables de entorno (secret keys, DB)
├── requirements.txt     # Librerías necesarias
└── README.md            # Este archivo
nstalación
1. Clona este repositorio o descarga los archivos.
2. Crea un entorno virtual:
   - En Windows:
     python -m venv venv
     venv\Scripts\activate
   - En macOS/Linux:
     python3 -m venv venv
     source venv/bin/activate
3. Instala las dependencias:
   pip install -r requirements.txt
4. Crea un archivo `.env` con el siguiente contenido:

   FLASK_SECRET_KEY=tu_clave_secreta
   JWT_SECRET_KEY=tu_clave_jwt
   DATABASE_URL=sqlite:///todo.db
 Ejecución del servidor
Ejecuta el siguiente comando:

python app.py

El servidor estará disponible en:
http://127.0.0.1:5000/
Endpoints disponibles
🔐 Autenticación
POST /register
Registra un nuevo usuario:
{
  "email": "correo@example.com",
  "password": "1234"
}
POST /login
Devuelve un token JWT si las credenciales son válidas:
{
  "email": "correo@example.com",
  "password": "1234"
}

Respuesta esperada:
{
  "token": "JWT_TOKEN"
}

Usa este token en las siguientes peticiones protegidas:
Authorization: Bearer JWT_TOKEN
 Endpoints de tareas (protegidos)
POST /tasks
Crea una nueva tarea:
{
  "title": "Estudiar",
  "description": "Repasar grafos"
}
GET /tasks
Devuelve todas las tareas del usuario autenticado.
PATCH /tasks/<id>
Marca una tarea como completada (por su ID).
 Proceso automático
Cada 10 minutos, el sistema elimina automáticamente todas las tareas marcadas como completadas, usando APScheduler.
Pruebas con Postman
1. Ejecuta POST /register para registrar un nuevo usuario.
2. Ejecuta POST /login para obtener un token JWT.
3. Copia el token y agrégalo en el header de las peticiones:
   Authorization: Bearer TU_TOKEN
4. Ejecuta los endpoints /tasks usando POST, GET y PATCH.

