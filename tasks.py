# tasks.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Task   # <-- asegúrate de que tu archivo se llame models.py, no model.py

tasks = Blueprint('tasks', __name__)

# task.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from model import db, User, Task

task_bp = Blueprint('task_bp', __name__)

# --- Registro ---
@task_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(msg='Email y password son obligatorios'), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(msg='Email ya registrado'), 400

    hashed = generate_password_hash(data['password'])
    user = User(email=data['email'], password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify(msg='Usuario registrado'), 201

# --- Login ---
@task_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(msg='Email y password son obligatorios'), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify(msg='Credenciales inválidas'), 401

    token = create_access_token(identity=user.id)
    return jsonify(token=token), 200

# --- Crear tarea ---
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify(msg='Title es obligatorio'), 400

    task = Task(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', '')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(msg='Tarea creada', id=task.id), 201

# --- Listar tareas ---
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify(tasks=[{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'completed': t.completed,
        'created_at': t.created_at.isoformat()
    } for t in tasks]), 200

# --- Completar tarea ---
@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
@jwt_required()
def complete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    task.completed = True
    db.session.commit()
    return jsonify(msg='Tarea completada'), 200
