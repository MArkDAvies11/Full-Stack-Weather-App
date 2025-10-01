from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, origins=['*'])

# In-memory storage for demo (Vercel doesn't support SQLite persistence)
users_data = []
favorites_data = []
weather_logs = []

# Load cities data
def get_cities():
    return [
        'New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Berlin', 'Moscow', 'Cairo',
        'Mumbai', 'Beijing', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
        'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Miami', 'Seattle',
        'Denver', 'Boston', 'Atlanta', 'Las Vegas', 'Detroit', 'Portland', 'Nashville'
    ]

@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        weather = {
            'name': city,
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
        return jsonify(weather), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forecast/<city>', methods=['GET'])
def get_forecast(city):
    try:
        forecast = {
            'city': city,
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
def cities():
    return jsonify(get_cities()), 200

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    global users_data
    
    if request.method == 'GET':
        return jsonify(users_data), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email are required'}), 400
        
        # Check if username exists
        if any(user['username'] == data['username'] for user in users_data):
            return jsonify({'error': 'Username already exists'}), 400
        
        user = {
            'id': len(users_data) + 1,
            'username': data['username'],
            'email': data['email'],
            'created_at': datetime.utcnow().isoformat()
        }
        users_data.append(user)
        
        return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['PATCH', 'DELETE'])
def user_by_id(user_id):
    global users_data
    
    user = next((u for u in users_data if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'PATCH':
        data = request.get_json()
        
        if 'username' in data:
            user['username'] = data['username']
        if 'email' in data:
            user['email'] = data['email']
        
        return jsonify(user), 200
    
    elif request.method == 'DELETE':
        users_data = [u for u in users_data if u['id'] != user_id]
        return '', 204

@app.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    global favorites_data
    
    if request.method == 'GET':
        return jsonify(favorites_data), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data.get('user_id') or not data.get('city_name'):
            return jsonify({'error': 'User ID and city name are required'}), 400
        
        # Check if already exists
        existing = next((f for f in favorites_data if f['user_id'] == data['user_id'] and f['city_name'] == data['city_name']), None)
        if existing:
            return jsonify({'error': 'City already in favorites'}), 400
        
        favorite = {
            'id': len(favorites_data) + 1,
            'user_id': data['user_id'],
            'city_name': data['city_name'],
            'created_at': datetime.utcnow().isoformat()
        }
        favorites_data.append(favorite)
        
        return jsonify(favorite), 201

@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    global favorites_data
    
    favorite = next((f for f in favorites_data if f['id'] == favorite_id), None)
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    favorites_data = [f for f in favorites_data if f['id'] != favorite_id]
    return '', 204

# Vercel serverless function handler
def handler(request, context):
    return app

if __name__ == '__main__':
    app.run(debug=True)