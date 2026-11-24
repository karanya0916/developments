from flask import Blueprint, render_template, session, redirect, url_for
from routes.auth import login_required
from services.analytics import get_dashboard_summary
from services.weather_service import get_current_weather

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    summary = get_dashboard_summary()
    weather = get_current_weather()
    return render_template(
        'dashboard.html',
        kpis=summary['kpis'],
        charts=summary['charts'],
        low_stock_materials=summary['low_stock_materials'],
        project_risks=summary['project_risks'],
        recent_diary=summary['recent_diary'],
        recent_tasks=summary['recent_tasks'],
        recent_leads=summary['recent_leads'],
        weather=weather,
        current_user=session
    )
