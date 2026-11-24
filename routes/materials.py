from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from routes.auth import login_required, role_required
from services.material_prediction import predict_material_requirements
from database.db import get_db_connection

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/inventory')
@login_required
def inventory():
    category = request.args.get('category', '')
    status = request.args.get('status', '') # low_stock

    conn = get_db_connection()
    query = "SELECT * FROM materials WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if status == 'low_stock':
        query += " AND current_stock <= min_threshold"

    query += " ORDER BY category ASC, name ASC"
    materials = conn.execute(query, params).fetchall()

    categories = [r['category'] for r in conn.execute("SELECT DISTINCT category FROM materials ORDER BY category").fetchall()]
    projects = conn.execute("SELECT id, name FROM projects WHERE status = 'In Progress'").fetchall()
    
    # Recent transactions
    transactions = conn.execute("""
        SELECT it.*, m.name as material_name, m.unit, p.name as project_name, u.full_name as logger_name
        FROM inventory_transactions it
        JOIN materials m ON it.material_id = m.id
        LEFT JOIN projects p ON it.project_id = p.id
        LEFT JOIN users u ON it.logged_by_id = u.id
        ORDER BY it.timestamp DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return render_template(
        'inventory.html',
        materials=materials,
        categories=categories,
        projects=projects,
        transactions=transactions,
        selected_category=category,
        selected_status=status
    )

@materials_bp.route('/inventory/add', methods=['POST'])
@login_required
@role_required(['Administrator', 'Inventory Manager', 'Project Manager'])
def add_material():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', 'Cement')
    brand = request.form.get('brand', '').strip()
    grade_spec = request.form.get('grade_spec', '')
    unit = request.form.get('unit', 'Bags')
    current_stock = float(request.form.get('current_stock', 0.0))
    min_threshold = float(request.form.get('min_threshold', 10.0))
    unit_price = float(request.form.get('unit_price', 0.0))
    supplier_name = request.form.get('supplier_name', '')
    supplier_phone = request.form.get('supplier_phone', '')
    location_in_site = request.form.get('location_in_site', '')

    if not name or not brand:
        flash('Material name and brand are required.', 'danger')
        return redirect(url_for('materials.inventory'))

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO materials (name, category, brand, grade_spec, unit, current_stock, min_threshold, unit_price, supplier_name, supplier_phone, location_in_site, is_mcb_approved)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1);
    """, (name, category, brand, grade_spec, unit, current_stock, min_threshold, unit_price, supplier_name, supplier_phone, location_in_site))
    conn.commit()
    conn.close()

    flash(f"Material '{name} ({brand})' added to inventory.", 'success')
    return redirect(url_for('materials.inventory'))

@materials_bp.route('/inventory/<int:material_id>/transaction', methods=['POST'])
@login_required
def record_transaction(material_id):
    transaction_type = request.form.get('transaction_type') # IN, OUT, WASTAGE, RETURN
    quantity = float(request.form.get('quantity', 0.0))
    project_id = request.form.get('project_id') or None
    reference_no = request.form.get('reference_no', '')
    notes = request.form.get('notes', '')

    if quantity <= 0:
        flash('Quantity must be greater than zero.', 'danger')
        return redirect(url_for('materials.inventory'))

    conn = get_db_connection()
    mat = conn.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    if not mat:
        conn.close()
        flash('Material not found.', 'danger')
        return redirect(url_for('materials.inventory'))

    new_stock = mat['current_stock']
    if transaction_type in ('IN', 'RETURN'):
        new_stock += quantity
    elif transaction_type in ('OUT', 'WASTAGE'):
        if quantity > mat['current_stock']:
            conn.close()
            flash(f"Insufficient stock! Available: {mat['current_stock']} {mat['unit']}", 'danger')
            return redirect(url_for('materials.inventory'))
        new_stock -= quantity

    total_amount = round(quantity * mat['unit_price'], 2)

    conn.execute("UPDATE materials SET current_stock = ? WHERE id = ?", (new_stock, material_id))
    conn.execute("""
    INSERT INTO inventory_transactions (material_id, project_id, transaction_type, quantity, unit_price, total_amount, reference_no, logged_by_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (material_id, project_id, transaction_type, quantity, mat['unit_price'], total_amount, reference_no, session.get('user_id'), notes))
    
    conn.commit()
    conn.close()

    flash(f"Stock transaction logged: {transaction_type} {quantity} {mat['unit']} for '{mat['name']}'.", 'success')
    return redirect(url_for('materials.inventory'))

@materials_bp.route('/materials/prediction', methods=['GET', 'POST'])
def prediction():
    prediction_result = None
    input_data = {
        'built_up_area': 2200,
        'floors': 2,
        'quality_tier': 'Premium',
        'building_type': 'Residential Villa',
        'location': 'Warangal'
    }

    if request.method == 'POST':
        built_up_area = float(request.form.get('built_up_area', 2200))
        floors = int(request.form.get('floors', 2))
        quality_tier = request.form.get('quality_tier', 'Premium')
        building_type = request.form.get('building_type', 'Residential Villa')
        location = request.form.get('location', 'Warangal')

        input_data = {
            'built_up_area': built_up_area,
            'floors': floors,
            'quality_tier': quality_tier,
            'building_type': building_type,
            'location': location
        }

        prediction_result = predict_material_requirements(
            built_up_area=built_up_area,
            floors=floors,
            quality_tier=quality_tier,
            building_type=building_type,
            location=location
        )

    return render_template(
        'prediction.html',
        prediction=prediction_result,
        input_data=input_data
    )

@materials_bp.route('/api/material-prediction', methods=['POST'])
def api_prediction():
    try:
        data = request.get_json() or {}
        built_up_area = float(data.get('built_up_area', 2000))
        floors = int(data.get('floors', 2))
        quality_tier = data.get('quality_tier', 'Premium')
        res = predict_material_requirements(built_up_area, floors, quality_tier)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
