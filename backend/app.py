from flask import Flask
from flask_cors import CORS
from backend.models import db
from backend.routes.weather_routes import weather_bp
from backend.routes.user_routes import user_bp
from backend.routes.favorite_routes import favorite_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'weather-app-secret'
    
    db.init_app(app)
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    app.register_blueprint(weather_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(favorite_bp)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')