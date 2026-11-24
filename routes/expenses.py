from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from routes.auth import login_required
from database.db import get_db_connection

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses')
@login_required
def index():
    project_id = request.args.get('project_id')
    category_filter = request.args.get('category')

    conn = get_db_connection()
    query = """
        SELECT e.*, p.name as project_name, p.code as project_code, u.full_name as approved_by_name
        FROM expenses e
        JOIN projects p ON e.project_id = p.id
        LEFT JOIN users u ON e.approved_by_id = u.id
        WHERE 1=1
    """
    params = []

    if project_id:
        query += " AND e.project_id = ?"
        params.append(project_id)

    if category_filter:
        query += " AND e.expense_category = ?"
        params.append(category_filter)

    query += " ORDER BY e.expense_date DESC, e.id DESC"
    expenses = conn.execute(query, params).fetchall()

    projects = conn.execute("SELECT id, name, code, budget, actual_cost FROM projects").fetchall()
    categories = ['Material', 'Labour', 'Equipment', 'Subcontract', 'Fuel & Transport', 'Permits & Approvals', 'Petty Cash', 'Miscellaneous']

    # Total expenses calculated
    total_spent = sum(float(e['amount']) for e in expenses)

    conn.close()

    return render_template(
        'expenses.html',
        expenses=expenses,
        projects=projects,
        categories=categories,
        selected_project=int(project_id) if project_id else None,
        selected_category=category_filter,
        total_spent=round(total_spent, 2),
        today=date.today().strftime('%Y-%m-%d')
    )

@expenses_bp.route('/expenses/add', methods=['POST'])
@login_required
def add_expense():
    project_id = request.form.get('project_id')
    expense_category = request.form.get('expense_category', 'Material')
    title = request.form.get('title', '').strip()
    amount = float(request.form.get('amount', 0.0))
    payment_mode = request.form.get('payment_mode', 'UPI/Online')
    paid_to = request.form.get('paid_to', '').strip()
    receipt_number = request.form.get('receipt_number', '').strip()
    expense_date = request.form.get('expense_date', date.today().strftime('%Y-%m-%d'))
    notes = request.form.get('notes', '')

    if not project_id or not title or amount <= 0:
        flash('Project, title, and a valid amount are required.', 'danger')
        return redirect(url_for('expenses.index'))

    conn = get_db_connection()
    conn.execute("""
    INSERT INTO expenses (project_id, expense_category, title, amount, payment_mode, paid_to, receipt_number, expense_date, approved_by_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (project_id, expense_category, title, amount, payment_mode, paid_to, receipt_number, expense_date, session.get('user_id'), notes))

    # Update actual_cost in projects
    conn.execute("UPDATE projects SET actual_cost = actual_cost + ? WHERE id = ?", (amount, project_id))
    conn.commit()
    conn.close()

    flash(f"Expense of ₹{amount:,.2f} recorded under '{expense_category}'.", 'success')
    return redirect(url_for('expenses.index', project_id=project_id))
