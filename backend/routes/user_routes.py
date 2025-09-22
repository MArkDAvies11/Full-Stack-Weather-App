from flask import Blueprint, request, jsonify
from backend.models import db, User

user_bp = Blueprint('users', __name__)

@user_bp.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username exists'}), 400
        
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201

@user_bp.route('/api/users/<int:user_id>', methods=['PATCH', 'DELETE'])
def user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'PATCH':
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204