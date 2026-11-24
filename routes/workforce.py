from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from routes.auth import login_required, role_required
from database.db import get_db_connection

workforce_bp = Blueprint('workforce', __name__)

@workforce_bp.route('/workforce')
@login_required
def index():
    skill_filter = request.args.get('skill', '')
    status_filter = request.args.get('status', 'Active')

    conn = get_db_connection()
    query = "SELECT * FROM workers WHERE 1=1"
    params = []

    if skill_filter:
        query += " AND skill_category = ?"
        params.append(skill_filter)

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY full_name ASC"
    workers = conn.execute(query, params).fetchall()

    skills = [r[0] for r in conn.execute("SELECT DISTINCT skill_category FROM workers ORDER BY skill_category").fetchall()]
    
    # Active projects for attendance logging
    projects = conn.execute("SELECT id, name FROM projects WHERE status = 'In Progress'").fetchall()
    conn.close()

    return render_template(
        'workforce.html',
        workers=workers,
        skills=skills,
        projects=projects,
        selected_skill=skill_filter,
        selected_status=status_filter,
        today=date.today().strftime('%Y-%m-%d')
    )

@workforce_bp.route('/workforce/add', methods=['POST'])
@login_required
@role_required(['Administrator', 'Project Manager', 'Site Engineer'])
def add_worker():
    full_name = request.form.get('full_name', '').strip()
    phone = request.form.get('phone', '').strip()
    skill_category = request.form.get('skill_category', 'General Labor')
    daily_wage_rate = float(request.form.get('daily_wage_rate', 700.0))
    aadhar_id = request.form.get('aadhar_id', '').strip()
    emergency_contact = request.form.get('emergency_contact', '').strip()
    joined_date = request.form.get('joined_date', date.today().strftime('%Y-%m-%d'))

    if not full_name or not phone:
        flash('Worker full name and contact phone are required.', 'danger')
        return redirect(url_for('workforce.index'))

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO workers (full_name, phone, skill_category, daily_wage_rate, status, aadhar_id, emergency_contact, joined_date)
    VALUES (?, ?, ?, ?, 'Active', ?, ?, ?);
    """, (full_name, phone, skill_category, daily_wage_rate, aadhar_id, emergency_contact, joined_date))
    conn.commit()
    conn.close()

    flash(f"Worker '{full_name}' registered under '{skill_category}'.", 'success')
    return redirect(url_for('workforce.index'))

@workforce_bp.route('/workforce/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    conn = get_db_connection()
    projects = conn.execute("SELECT id, name FROM projects WHERE status = 'In Progress'").fetchall()
    
    selected_project = request.args.get('project_id', projects[0]['id'] if projects else None)
    selected_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        att_date = request.form.get('date')
        worker_ids = request.form.getlist('worker_id[]')

        for wid in worker_ids:
            status = request.form.get(f'status_{wid}', 'Present')
            hours = float(request.form.get(f'hours_{wid}', 8.0))
            ot = float(request.form.get(f'ot_{wid}', 0.0))
            rate = float(request.form.get(f'rate_{wid}', 700.0))

            if status == 'Present':
                earning = rate + (ot * (rate / 8.0) * 1.5)
            elif status == 'Half Day':
                earning = (rate / 2.0) + (ot * (rate / 8.0) * 1.5)
            else:
                earning = 0.0

            # Insert or replace
            conn.execute("""
            INSERT OR REPLACE INTO attendance (worker_id, project_id, date, status, hours_worked, overtime_hours, daily_earning, recorded_by_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (wid, project_id, att_date, status, hours, ot, round(earning, 2), session.get('user_id')))

        conn.commit()
        flash(f"Attendance for {att_date} recorded successfully!", 'success')
        conn.close()
        return redirect(url_for('workforce.attendance', project_id=project_id, date=att_date))

    # Fetch workers and existing attendance for selected date
    workers = conn.execute("SELECT * FROM workers WHERE status = 'Active' ORDER BY skill_category ASC, full_name ASC").fetchall()
    existing_att = {
        row['worker_id']: row for row in conn.execute(
            "SELECT * FROM attendance WHERE project_id = ? AND date = ?", (selected_project, selected_date)
        ).fetchall()
    }
    conn.close()

    return render_template(
        'attendance.html',
        projects=projects,
        workers=workers,
        existing_att=existing_att,
        selected_project=int(selected_project) if selected_project else None,
        selected_date=selected_date
    )
