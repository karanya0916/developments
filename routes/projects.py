from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth import login_required, role_required
from database.db import get_db_connection

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
@login_required
def list_projects():
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '').strip()

    conn = get_db_connection()
    query = """
        SELECT p.*, 
               u1.full_name as manager_name, 
               u2.full_name as engineer_name,
               (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id) as total_tasks,
               (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id AND t.status = 'Completed') as completed_tasks
        FROM projects p
        LEFT JOIN users u1 ON p.project_manager_id = u1.id
        LEFT JOIN users u2 ON p.site_engineer_id = u2.id
        WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND p.status = ?"
        params.append(status_filter)

    if search:
        query += " AND (p.name LIKE ? OR p.code LIKE ? OR p.client_name LIKE ? OR p.location LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term])

    query += " ORDER BY p.id DESC"
    projects = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('projects.html', projects=projects, current_status=status_filter, search=search)

@projects_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@role_required(['Administrator', 'Project Manager'])
def create_project():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        code = request.form.get('code', '').strip()
        client_name = request.form.get('client_name', '').strip()
        client_phone = request.form.get('client_phone', '').strip()
        location = request.form.get('location', '').strip()
        building_type = request.form.get('building_type', 'Residential Villa')
        plot_area = float(request.form.get('plot_area', 0.0))
        built_up_area = float(request.form.get('built_up_area', 0.0))
        floors = int(request.form.get('floors', 1))
        budget = float(request.form.get('budget', 0.0))
        start_date = request.form.get('start_date')
        deadline = request.form.get('deadline')
        pm_id = request.form.get('project_manager_id') or None
        eng_id = request.form.get('site_engineer_id') or None
        description = request.form.get('description', '')

        if not name or not code or not client_name or not location or not start_date or not deadline:
            flash('Please fill in all mandatory fields.', 'danger')
            users = conn.execute("SELECT id, full_name, role FROM users").fetchall()
            conn.close()
            return render_template('project_form.html', project=None, users=users)

        try:
            conn.execute("""
            INSERT INTO projects (name, code, client_name, client_phone, location, building_type, plot_area, built_up_area, floors, budget, start_date, deadline, status, project_manager_id, site_engineer_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Planning', ?, ?, ?);
            """, (name, code, client_name, client_phone, location, building_type, plot_area, built_up_area, floors, budget, start_date, deadline, pm_id, eng_id, description))
            conn.commit()
            conn.close()
            flash(f"Project '{name}' created successfully!", 'success')
            return redirect(url_for('projects.list_projects'))
        except Exception as e:
            conn.close()
            flash(f"Error creating project: {str(e)}", 'danger')
            return redirect(url_for('projects.create_project'))

    users = conn.execute("SELECT id, full_name, role FROM users").fetchall()
    conn.close()
    return render_template('project_form.html', project=None, users=users)

@projects_bp.route('/projects/<int:project_id>')
@login_required
def view_project(project_id):
    conn = get_db_connection()
    project = conn.execute("""
        SELECT p.*, u1.full_name as manager_name, u2.full_name as engineer_name
        FROM projects p
        LEFT JOIN users u1 ON p.project_manager_id = u1.id
        LEFT JOIN users u2 ON p.site_engineer_id = u2.id
        WHERE p.id = ?
    """, (project_id,)).fetchone()

    if not project:
        conn.close()
        flash('Project not found.', 'danger')
        return redirect(url_for('projects.list_projects'))

    tasks = conn.execute("""
        SELECT t.*, u.full_name as assignee_name
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to_id = u.id
        WHERE t.project_id = ?
        ORDER BY t.due_date ASC
    """, (project_id,)).fetchall()

    expenses = conn.execute("""
        SELECT * FROM expenses WHERE project_id = ? ORDER BY expense_date DESC LIMIT 10
    """, (project_id,)).fetchall()

    diary_entries = conn.execute("""
        SELECT * FROM site_diary WHERE project_id = ? ORDER BY entry_date DESC LIMIT 5
    """, (project_id,)).fetchall()

    images = conn.execute("""
        SELECT * FROM site_images WHERE project_id = ? ORDER BY uploaded_at DESC
    """, (project_id,)).fetchall()

    users = conn.execute("SELECT id, full_name, role FROM users").fetchall()
    conn.close()

    return render_template(
        'project_detail.html',
        project=project,
        tasks=tasks,
        expenses=expenses,
        diary_entries=diary_entries,
        images=images,
        users=users
    )

@projects_bp.route('/projects/<int:project_id>/tasks/add', methods=['POST'])
@login_required
def add_task(project_id):
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    assigned_to_id = request.form.get('assigned_to_id') or None
    start_date = request.form.get('start_date')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority', 'Medium')

    if not title:
        flash('Task title is required.', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO tasks (project_id, title, description, assigned_to_id, start_date, due_date, priority, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending');
    """, (project_id, title, description, assigned_to_id, start_date, due_date, priority))
    conn.commit()
    conn.close()

    flash('Task added successfully.', 'success')
    return redirect(url_for('projects.view_project', project_id=project_id))

@projects_bp.route('/projects/tasks/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    status = request.form.get('status')
    completion = float(request.form.get('completion_percentage', 0.0))
    project_id = request.form.get('project_id')

    conn = get_db_connection()
    conn.execute("""
    UPDATE tasks 
    SET status = ?, completion_percentage = ?
    WHERE id = ?;
    """, (status, completion, task_id))

    # Recalculate project overall completion percentage
    all_tasks = conn.execute("SELECT completion_percentage FROM tasks WHERE project_id = ?", (project_id,)).fetchall()
    if all_tasks:
        avg_pct = round(sum(t['completion_percentage'] for t in all_tasks) / len(all_tasks), 1)
        conn.execute("UPDATE projects SET completion_percentage = ? WHERE id = ?", (avg_pct, project_id))

    conn.commit()
    conn.close()

    flash('Task status updated successfully.', 'success')
    return redirect(url_for('projects.view_project', project_id=project_id))
