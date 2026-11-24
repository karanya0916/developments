from flask import Blueprint, render_template, request
from routes.auth import login_required
from services.weather_service import get_current_weather

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather')
@login_required
def index():
    location = request.args.get('location', 'Warangal, Telangana')
    weather_info = get_current_weather(location=location)
    return render_template('weather.html', weather=weather_info)
