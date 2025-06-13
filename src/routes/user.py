# Conteúdo para: src/routes/user.py

from flask import Blueprint, jsonify, request
from src.models.user import db, User
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Dados incompletos."}), 400

    
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"error": "Email já cadastrado."}), 409

    hashed_password = generate_password_hash(password)
    
    sql = text("""
        INSERT INTO users (name, email, password_hash, level) 
        VALUES (:name, :email, :password_hash, :level)
    """)
    try:
        db.session.execute(sql, {
            "name": name, 
            "email": email, 
            "password_hash": hashed_password,
            "level": "user" 
        })
        db.session.commit()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao registrar usuário: {str(e)}"}), 500

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"error": "Credenciais inválidas."}), 401

    return jsonify({
        "message": "Login bem-sucedido!",
        "user": user.to_dict()
    })


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    sql = text("UPDATE users SET name = :name, email = :email, level = :level WHERE id = :id")
    try:
        result = db.session.execute(sql, {
            "name": data.get('name'),
            "email": data.get('email'),
            "level": data.get('level'),
            "id": id
        })
        if result.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado."}), 404
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar usuário: {str(e)}"}), 500

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    sql = text("DELETE FROM users WHERE id = :id")
    try:
        result = db.session.execute(sql, {"id": id})
        if result.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado."}), 404
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar usuário: {str(e)}"}), 500