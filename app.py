import os
from flask import Flask, render_template, send_from_directory, session
from config import Config
from database.db import init_db

# Initialize Flask application
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
)
app.config.from_object(Config)

# Ensure essential directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'ml_models'), exist_ok=True)

# Initialize database schema if not already initialized
with app.app_context():
    init_db()

# Register Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.projects import projects_bp
from routes.estimation import estimation_bp
from routes.materials import materials_bp
from routes.workforce import workforce_bp
from routes.site_diary import site_diary_bp
from routes.expenses import expenses_bp
from routes.progress import progress_bp
from routes.weather import weather_bp
from routes.chatbot import chatbot_bp
from routes.public import public_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(estimation_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(workforce_bp)
app.register_blueprint(site_diary_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(public_bp)

# Context processor for global branding and builder details
@app.context_processor
def inject_global_data():
    return {
        "company_name": "MAMATHA CONSTRUCTIONS & BUILDERS",
        "company_short": "MCB CONSTRUCTIONS",
        "primary_builder": "SARGU SANJU",
        "office_address": "Vishwanath Colony, Near Hanuman Temple, Shambunipet, Warangal, Telangana 506005",
        "primary_phone": "7386181866",
        "current_user": session,
        "current_year": 2026,
        "current_lang": session.get('lang', 'en')
    }

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Local development server
    app.run(host='0.0.0.0', port=5000, debug=True)
