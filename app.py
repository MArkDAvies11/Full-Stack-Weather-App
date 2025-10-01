from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy_serializer import SerializerMixin
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

# Models
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    
    serialize_rules = ('-favorites.user',)

class City(db.Model, SerializerMixin):
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(10), nullable=False)
    
    favorites = db.relationship('Favorite', back_populates='city', cascade='all, delete-orphan')
    weather_logs = db.relationship('WeatherLog', back_populates='city', cascade='all, delete-orphan')
    
    serialize_rules = ('-favorites.city', '-weather_logs.city')

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='favorites')
    city = db.relationship('City', back_populates='favorites')
    
    serialize_rules = ('-user.favorites', '-city.favorites')

class WeatherLog(db.Model, SerializerMixin):
    __tablename__ = 'weather_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    city = db.relationship('City', back_populates='weather_logs')
    
    serialize_rules = ('-city.weather_logs',)

# Routes
@app.route('/api/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    try:
        # Mock weather data for demo
        import random
        
        mock_data = {
            'name': city_name,
            'main': {
                'temp': round(random.uniform(15, 30), 1),
                'humidity': random.randint(40, 80)
            },
            'weather': [{
                'description': random.choice(['sunny', 'cloudy', 'partly cloudy', 'light rain'])
            }],
            'wind': {
                'speed': round(random.uniform(2, 15), 1)
            }
        }
        
        # Log weather data
        city = City.query.filter_by(name=city_name).first()
        if not city:
            city = City(name=city_name, country='Unknown')
            db.session.add(city)
            db.session.commit()
        
        weather_log = WeatherLog(
            city_id=city.id,
            temperature=mock_data['main']['temp'],
            description=mock_data['weather'][0]['description'],
            humidity=mock_data['main']['humidity'],
            wind_speed=mock_data['wind']['speed']
        )
        db.session.add(weather_log)
        db.session.commit()
        
        return jsonify(mock_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email are required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
def user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'PATCH':
        data = request.get_json()
        
        if 'username' in data:
            if User.query.filter_by(username=data['username']).filter(User.id != user_id).first():
                return jsonify({'error': 'Username already exists'}), 400
            user.username = data['username']
        
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204

@app.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'GET':
        favorites = Favorite.query.all()
        return jsonify([fav.to_dict() for fav in favorites]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('user_id') or not data.get('city_name'):
            return jsonify({'error': 'User ID and city name are required'}), 400
        
        city = City.query.filter_by(name=data['city_name']).first()
        if not city:
            city = City(name=data['city_name'], country=data.get('country', 'Unknown'))
            db.session.add(city)
            db.session.commit()
        
        existing = Favorite.query.filter_by(user_id=data['user_id'], city_id=city.id).first()
        if existing:
            return jsonify({'error': 'City already in favorites'}), 400
        
        favorite = Favorite(user_id=data['user_id'], city_id=city.id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify(favorite.to_dict()), 201

@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204

@app.route('/api/forecast/<city_name>', methods=['GET'])
def get_forecast(city_name):
    try:
        import random
        from datetime import timedelta
        
        forecast = {
            'city': city_name,
            'forecast': []
        }
        
        for i in range(5):
            day_forecast = {
                'day': i + 1,
                'temperature': round(random.uniform(15, 30), 1),
                'humidity': random.randint(40, 80),
                'condition': random.choice(['sunny', 'cloudy', 'partly cloudy', 'light rain']),
                'date': (datetime.utcnow() + timedelta(days=i)).strftime('%Y-%m-%d')
            }
            forecast['forecast'].append(day_forecast)
        
        return jsonify(forecast), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cities', methods=['GET'])
def get_cities():
    import json
    with open('cities.json', 'r') as f:
        cities = json.load(f)
    return jsonify(cities), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)