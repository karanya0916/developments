import os
import json
from datetime import datetime, date
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from routes.auth import login_required
from database.db import get_db_connection

site_diary_bp = Blueprint('site_diary', __name__)

@site_diary_bp.route('/site-diary')
@login_required
def index():
    project_id = request.args.get('project_id')
    date_filter = request.args.get('date')

    conn = get_db_connection()
    query = """
        SELECT sd.*, p.name as project_name, p.code as project_code, u.full_name as author_name
        FROM site_diary sd
        JOIN projects p ON sd.project_id = p.id
        LEFT JOIN users u ON sd.logged_by_id = u.id
        WHERE 1=1
    """
    params = []

    if project_id:
        query += " AND sd.project_id = ?"
        params.append(project_id)

    if date_filter:
        query += " AND sd.entry_date = ?"
        params.append(date_filter)

    query += " ORDER BY sd.entry_date DESC, sd.id DESC"
    entries = conn.execute(query, params).fetchall()

    projects = conn.execute("SELECT id, name, code FROM projects WHERE status IN ('In Progress', 'Planning')").fetchall()
    conn.close()

    parsed_entries = []
    for entry in entries:
        item = dict(entry)
        try:
            item['petty_expenses'] = json.loads(entry['petty_expenses_json']) if entry['petty_expenses_json'] else []
        except Exception:
            item['petty_expenses'] = []
        try:
            item['photos'] = json.loads(entry['photos_json']) if entry['photos_json'] else []
        except Exception:
            item['photos'] = []
        parsed_entries.append(item)

    return render_template(
        'site_diary.html',
        entries=parsed_entries,
        projects=projects,
        selected_project=project_id,
        selected_date=date_filter,
        today=date.today().strftime('%Y-%m-%d')
    )

@site_diary_bp.route('/site-diary/new', methods=['GET', 'POST'])
@login_required
def create_entry():
    conn = get_db_connection()
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        entry_date = request.form.get('entry_date', date.today().strftime('%Y-%m-%d'))
        weather_condition = request.form.get('weather_condition', 'Clear & Sunny')
        temperature = float(request.form.get('temperature', 31.0))
        shift_type = request.form.get('shift_type', 'Day Shift')
        work_carried_out = request.form.get('work_carried_out', '').strip()
        challenges_issues = request.form.get('challenges_issues', '').strip()
        workers_count = int(request.form.get('workers_count', 0))
        engineer_signature = request.form.get('engineer_signature', session.get('full_name', 'Site Engineer'))

        if not project_id or not work_carried_out:
            flash('Project and detailed description of work carried out are required.', 'danger')
            projects = conn.execute("SELECT id, name FROM projects").fetchall()
            conn.close()
            return render_template('site_diary_form.html', projects=projects, today=entry_date)

        # Parse Dynamic Daily On-Site Expenses Table (Petty Cash Items)
        item_names = request.form.getlist('expense_item[]')
        item_amounts = request.form.getlist('expense_amount[]')
        item_paids = request.form.getlist('expense_paid_to[]')
        item_cats = request.form.getlist('expense_category[]')

        petty_expenses = []
        daily_expense_total = 0.0

        for i in range(len(item_names)):
            name = item_names[i].strip() if i < len(item_names) else ''
            if name:
                try:
                    amt = float(item_amounts[i]) if i < len(item_amounts) and item_amounts[i] else 0.0
                except ValueError:
                    amt = 0.0
                paid_to = item_paids[i].strip() if i < len(item_paids) else ''
                cat = item_cats[i].strip() if i < len(item_cats) else 'Petty Cash'

                petty_expenses.append({
                    "item": name,
                    "amount": amt,
                    "paid_to": paid_to,
                    "category": cat
                })
                daily_expense_total += amt

        # Handle Photo uploads if any
        photos = []
        uploaded_files = request.files.getlist('site_photos')
        upload_dir = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)

        for file in uploaded_files:
            if file and file.filename:
                fname = secure_filename(f"diary_{project_id}_{entry_date}_{file.filename}")
                filepath = os.path.join(upload_dir, fname)
                file.save(filepath)
                rel_path = url_for('uploaded_file', filename=fname)
                photos.append(rel_path)

        if not photos:
            # Default placeholder image if none uploaded
            photos = ['/static/images/portfolio_project_2.jpg']

        try:
            # 1. Insert into site_diary table
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO site_diary (
                project_id, entry_date, weather_condition, temperature, shift_type,
                work_carried_out, challenges_issues, workers_count, daily_expense_total,
                petty_expenses_json, photos_json, logged_by_id, engineer_signature, verified_by_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                project_id, entry_date, weather_condition, temperature, shift_type,
                work_carried_out, challenges_issues, workers_count, daily_expense_total,
                json.dumps(petty_expenses), json.dumps(photos), session.get('user_id'),
                engineer_signature, session.get('user_id')
            ))

            # 2. Also register petty expenses into master expenses table for accounting audit
            if daily_expense_total > 0:
                cursor.execute("""
                INSERT INTO expenses (project_id, expense_category, title, amount, payment_mode, paid_to, expense_date, approved_by_id, notes)
                VALUES (?, 'Petty Cash', ?, ?, 'Cash', 'On-Site Petty Cash Log', ?, ?, ?);
                """, (
                    project_id,
                    f"Site Daily Expenses ({entry_date} - {len(petty_expenses)} items)",
                    daily_expense_total,
                    entry_date,
                    session.get('user_id'),
                    f"Logged via Site Diary by {session.get('full_name')} for {shift_type}"
                ))

                # Update actual_cost in project
                cursor.execute("""
                UPDATE projects 
                SET actual_cost = actual_cost + ? 
                WHERE id = ?;
                """, (daily_expense_total, project_id))

            conn.commit()
            conn.close()
            flash(f"Site Diary for {entry_date} logged successfully! Total on-site expense: ₹{daily_expense_total:,.2f}", 'success')
            return redirect(url_for('site_diary.index'))

        except Exception as e:
            conn.close()
            flash(f"Error saving site diary entry: {str(e)}", 'danger')
            return redirect(url_for('site_diary.create_entry'))

    projects = conn.execute("SELECT id, name, code FROM projects WHERE status IN ('In Progress', 'Planning')").fetchall()
    conn.close()
    return render_template(
        'site_diary_form.html',
        projects=projects,
        today=date.today().strftime('%Y-%m-%d'),
        engineer_name=session.get('full_name', 'Site Engineer')
    )

@site_diary_bp.route('/site-diary/<int:entry_id>')
@login_required
def view_entry(entry_id):
    conn = get_db_connection()
    entry = conn.execute("""
        SELECT sd.*, p.name as project_name, p.code as project_code, p.location as project_location,
               p.client_name, u.full_name as author_name, u.role as author_role
        FROM site_diary sd
        JOIN projects p ON sd.project_id = p.id
        LEFT JOIN users u ON sd.logged_by_id = u.id
        WHERE sd.id = ?
    """, (entry_id,)).fetchone()
    conn.close()

    if not entry:
        flash('Diary entry not found.', 'danger')
        return redirect(url_for('site_diary.index'))

    entry_data = dict(entry)
    entry_data['petty_expenses'] = json.loads(entry['petty_expenses_json']) if entry['petty_expenses_json'] else []
    entry_data['photos'] = json.loads(entry['photos_json']) if entry['photos_json'] else []

    return render_template('site_diary_detail.html', entry=entry_data)
