from flask import Blueprint, request, jsonify
from backend.models import db, Favorite, Location

favorite_bp = Blueprint('favorites', __name__)

@favorite_bp.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'GET':
        favorites = Favorite.query.all()
        favorites_data = []
        for fav in favorites:
            fav_dict = fav.to_dict()
            fav_dict['user'] = fav.user.to_dict() if fav.user else None
            fav_dict['location'] = fav.location.to_dict() if fav.location else None
            favorites_data.append(fav_dict)
        return jsonify(favorites_data), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('user_id') or not data.get('city_name'):
            return jsonify({'error': 'User ID and city name required'}), 400
        
        location = Location.query.filter_by(name=data['city_name']).first()
        if not location:
            location = Location(
                name=data['city_name'],
                country='Unknown',
                latitude=0.0,
                longitude=0.0
            )
            db.session.add(location)
            db.session.commit()
        
        existing = Favorite.query.filter_by(user_id=data['user_id'], location_id=location.id).first()
        if existing:
            return jsonify({'error': 'Already in favorites'}), 400
        
        favorite = Favorite(user_id=data['user_id'], location_id=location.id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify(favorite.to_dict()), 201

@favorite_bp.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204