from flask import Flask
from flask_cors import CORS
from src.routes import (
    subscription_plan_bp, 
    subscription_bp, 
    subscription_plan_variation_bp
)
from src.database import engine
from src.models.base import Base
from src.middleware.auth import requires_auth
from src.middleware.rate_limiter import limiter
import os

def create_app():
    app = Flask(__name__)
    
    # Security and Performance Configurations
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'development_secret')
    
    # Rate Limiting
    limiter.init_app(app)
    
    # Database Setup
    Base.metadata.create_all(bind=engine)
    
    # Register Blueprints
    app.register_blueprint(subscription_plan_bp, url_prefix='/api/v1')
    app.register_blueprint(subscription_bp, url_prefix='/api/v1')
    app.register_blueprint(subscription_plan_variation_bp, url_prefix='/api/v1')
    
    # Health Check Endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)