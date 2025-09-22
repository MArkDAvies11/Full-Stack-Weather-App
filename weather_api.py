from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy_serializer import SerializerMixin
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'weather-api-key'

db = SQLAlchemy(app)
CORS(app)

# Models
class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    weather_data = db.relationship('WeatherData', back_populates='location', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='location', cascade='all, delete-orphan')

class WeatherData(db.Model, SerializerMixin):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    location = db.relationship('Location', back_populates='weather_data')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='favorites')
    location = db.relationship('Location', back_populates='favorites')

# API Routes
@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        # Generate mock weather data
        weather = {
            'city': city,
            'temperature': round(random.uniform(10, 35), 1),
            'humidity': random.randint(30, 90),
            'wind_speed': round(random.uniform(0, 20), 1),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Windy']),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store in database
        location = Location.query.filter_by(name=city).first()
        if not location:
            location = Location(
                name=city,
                country='Unknown',
                latitude=round(random.uniform(-90, 90), 4),
                longitude=round(random.uniform(-180, 180), 4)
            )
            db.session.add(location)
            db.session.commit()
        
        weather_data = WeatherData(
            location_id=location.id,
            temperature=weather['temperature'],
            humidity=weather['humidity'],
            wind_speed=weather['wind_speed'],
            condition=weather['condition']
        )
        db.session.add(weather_data)
        db.session.commit()
        
        return jsonify(weather), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = [
        'New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Berlin', 'Moscow', 'Cairo',
        'Mumbai', 'Beijing', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
        'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Miami', 'Seattle',
        'Denver', 'Boston', 'Atlanta', 'Las Vegas', 'Detroit', 'Portland', 'Nashville'
    ]
    return jsonify(cities), 200

@app.route('/api/users', methods=['GET', 'POST'])
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

@app.route('/api/users/<int:user_id>', methods=['PATCH', 'DELETE'])
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

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([loc.to_dict() for loc in locations]), 200

@app.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'GET':
        favorites = Favorite.query.all()
        return jsonify([fav.to_dict() for fav in favorites]), 200
    
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

@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)