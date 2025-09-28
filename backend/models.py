from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    serialize_rules = ('-weather_data', '-favorites')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    weather_data = db.relationship('WeatherData', back_populates='location', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='location', cascade='all, delete-orphan')

class WeatherData(db.Model, SerializerMixin):
    __tablename__ = 'weather_data'
    serialize_rules = ('-location',)
    
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
    serialize_rules = ('-favorites',)
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'
    serialize_rules = ('-user.favorites', '-location.favorites')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='favorites')
    location = db.relationship('Location', back_populates='favorites')