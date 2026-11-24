import os
from datetime import datetime, date
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from routes.auth import login_required
from services.image_analysis import analyze_site_image
from database.db import get_db_connection

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress')
@login_required
def index():
    project_id = request.args.get('project_id')

    conn = get_db_connection()
    projects = conn.execute("SELECT id, name, code, completion_percentage, status FROM projects").fetchall()
    
    current_proj_id = int(project_id) if project_id else (projects[0]['id'] if projects else None)

    images = []
    reports = []
    selected_project = None

    if current_proj_id:
        selected_project = conn.execute("SELECT * FROM projects WHERE id = ?", (current_proj_id,)).fetchone()
        images = conn.execute("""
            SELECT si.*, u.full_name as uploader_name
            FROM site_images si
            LEFT JOIN users u ON si.uploaded_by_id = u.id
            WHERE si.project_id = ?
            ORDER BY si.uploaded_at DESC
        """, (current_proj_id,)).fetchall()

        reports = conn.execute("""
            SELECT pr.*, u.full_name as author_name
            FROM progress_reports pr
            LEFT JOIN users u ON pr.submitted_by_id = u.id
            WHERE pr.project_id = ?
            ORDER BY pr.report_date DESC
        """, (current_proj_id,)).fetchall()

    conn.close()

    return render_template(
        'progress.html',
        projects=projects,
        selected_project=selected_project,
        images=images,
        reports=reports,
        today=date.today().strftime('%Y-%m-%d')
    )

@progress_bp.route('/progress/upload-image', methods=['POST'])
@login_required
def upload_image():
    project_id = request.form.get('project_id')
    manual_stage = request.form.get('stage_category', 'RCC_Framing')
    notes = request.form.get('notes', '')
    file = request.files.get('site_image')

    if not file or not file.filename:
        flash('Please select an image file to upload.', 'danger')
        return redirect(url_for('progress.index', project_id=project_id))

    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    fname = secure_filename(f"site_p{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
    filepath = os.path.join(upload_dir, fname)
    file.save(filepath)

    rel_path = url_for('uploaded_file', filename=fname)

    # Analyze with TensorFlow CNN model
    ai_analysis = analyze_site_image(filepath)
    ai_stage = ai_analysis.get('detected_stage', manual_stage)
    ai_conf = ai_analysis.get('confidence_percentage', 90.0) / 100.0

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO site_images (project_id, image_path, thumbnail_path, stage_category, ai_detected_stage, ai_confidence, inspection_status, notes, uploaded_by_id)
    VALUES (?, ?, ?, ?, ?, ?, 'Approved', ?, ?);
    """, (project_id, rel_path, rel_path, manual_stage, ai_stage, ai_conf, notes, session.get('user_id')))
    conn.commit()
    conn.close()

    flash(f"Image uploaded! TensorFlow AI classified stage as '{ai_stage}' ({ai_conf * 100:.1f}% confidence).", 'success')
    return redirect(url_for('progress.index', project_id=project_id))

@progress_bp.route('/progress/report/add', methods=['POST'])
@login_required
def add_report():
    project_id = request.form.get('project_id')
    report_date = request.form.get('report_date', date.today().strftime('%Y-%m-%d'))
    milestone_name = request.form.get('milestone_name', '').strip()
    planned_pct = float(request.form.get('planned_percentage', 0.0))
    actual_pct = float(request.form.get('actual_percentage', 0.0))
    variance = round(actual_pct - planned_pct, 1)
    activities_completed = request.form.get('activities_completed', '')
    pending_activities = request.form.get('pending_activities', '')
    delay_reasons = request.form.get('delay_reasons', '')
    corrective_action = request.form.get('corrective_action', '')

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO progress_reports (project_id, report_date, milestone_name, planned_percentage, actual_percentage, variance_percentage, activities_completed, pending_activities, delay_reasons, corrective_action, submitted_by_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (project_id, report_date, milestone_name, planned_pct, actual_pct, variance, activities_completed, pending_activities, delay_reasons, corrective_action, session.get('user_id')))

    # Update project completion percentage
    conn.execute("UPDATE projects SET completion_percentage = ? WHERE id = ?", (actual_pct, project_id))
    conn.commit()
    conn.close()

    flash(f"Progress report for '{milestone_name}' recorded. Project completion updated to {actual_pct}%.", 'success')
    return redirect(url_for('progress.index', project_id=project_id))
