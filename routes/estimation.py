from flask import Blueprint, render_template, request, jsonify, flash, session, redirect, url_for
from routes.auth import login_required
from services.cost_estimation import estimate_construction_cost
from database.db import get_db_connection
import json

estimation_bp = Blueprint('estimation', __name__)

@estimation_bp.route('/estimation', methods=['GET', 'POST'])
def index():
    estimate_result = None
    input_data = {
        'built_up_area': 2000,
        'plot_area': 1800,
        'floors': 2,
        'building_type': 'Residential Villa',
        'quality_tier': 'Premium',
        'location': 'Warangal'
    }

    if request.method == 'POST':
        try:
            built_up_area = float(request.form.get('built_up_area', 2000))
            plot_area = float(request.form.get('plot_area', 1800))
            floors = int(request.form.get('floors', 2))
            building_type = request.form.get('building_type', 'Residential Villa')
            quality_tier = request.form.get('quality_tier', 'Premium')
            location = request.form.get('location', 'Warangal')

            input_data = {
                'built_up_area': built_up_area,
                'plot_area': plot_area,
                'floors': floors,
                'building_type': building_type,
                'quality_tier': quality_tier,
                'location': location
            }

            estimate_result = estimate_construction_cost(
                built_up_area=built_up_area,
                floors=floors,
                quality_tier=quality_tier,
                building_type=building_type,
                location=location
            )

            # If user is logged in and requested save to database
            if 'user_id' in session and request.form.get('save_estimate'):
                client_name = request.form.get('client_name', 'Prospective Client')
                conn = get_db_connection()
                conn.execute("""
                INSERT INTO cost_estimates (client_name, building_type, plot_area, built_up_area, floors, quality_tier, location, estimated_total_cost, civil_cost, finishing_cost, mep_cost, labour_cost, material_breakdown_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    client_name, building_type, plot_area, built_up_area, floors, quality_tier, location,
                    estimate_result['recommended_budget'],
                    estimate_result['engineering_estimate']['civil_cost'],
                    estimate_result['engineering_estimate']['finishing_cost'],
                    estimate_result['engineering_estimate']['mep_cost'],
                    estimate_result['engineering_estimate']['labour_cost'],
                    json.dumps(estimate_result['engineering_estimate']['breakdown_items'])
                ))
                conn.commit()
                conn.close()
                flash('Estimate saved successfully to project records!', 'success')

        except Exception as e:
            flash(f"Error calculating estimate: {str(e)}", 'danger')

    return render_template(
        'estimation.html',
        estimate=estimate_result,
        input_data=input_data
    )

@estimation_bp.route('/api/estimate', methods=['POST'])
def api_estimate():
    try:
        data = request.get_json() or {}
        built_up_area = float(data.get('built_up_area', 2000))
        floors = int(data.get('floors', 2))
        quality_tier = data.get('quality_tier', 'Premium')
        building_type = data.get('building_type', 'Residential Villa')
        location = data.get('location', 'Warangal')

        res = estimate_construction_cost(built_up_area, floors, quality_tier, building_type, location)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
