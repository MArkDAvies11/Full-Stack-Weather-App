from flask import Blueprint, jsonify
from backend.models import db, Location, WeatherData
import random
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        weather = {
            'city': city,
            'temperature': round(random.uniform(10, 35), 1),
            'humidity': random.randint(30, 90),
            'wind_speed': round(random.uniform(0, 20), 1),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Windy']),
            'timestamp': datetime.utcnow().isoformat()
        }
        
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

@weather_bp.route('/api/cities', methods=['GET'])
def get_cities():
    cities = [
        'New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Berlin', 'Moscow', 'Cairo',
        'Mumbai', 'Beijing', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
        'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Miami', 'Seattle',
        'Denver', 'Boston', 'Atlanta', 'Las Vegas', 'Detroit', 'Portland', 'Nashville'
    ]
    return jsonify(cities), 200