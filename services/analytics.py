import os
import joblib
import numpy as np
from database.db import get_db_connection

DELAY_MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'ml_models', 'delay_risk_model.pkl')
_delay_model = None

def get_delay_model():
    global _delay_model
    if _delay_model is None and os.path.exists(DELAY_MODEL_PATH):
        try:
            _delay_model = joblib.load(DELAY_MODEL_PATH)
        except Exception as e:
            print(f"Error loading delay risk model: {e}")
            _delay_model = None
    return _delay_model

def get_dashboard_summary():
    """
    Computes key performance indicators (KPIs), financial metrics,
    material warehouse health, workforce status, and recent project progress.
    """
    conn = get_db_connection()
    
    # 1. Project Statistics
    projects = conn.execute("SELECT * FROM projects").fetchall()
    total_projects = len(projects)
    active_projects = sum(1 for p in projects if p['status'] == 'In Progress')
    completed_projects = sum(1 for p in projects if p['status'] == 'Completed')
    delayed_projects = sum(1 for p in projects if p['status'] == 'Delayed')
    planning_projects = sum(1 for p in projects if p['status'] == 'Planning')
    
    total_estimated_budget = sum(float(p['budget']) for p in projects)
    total_actual_expenditure = sum(float(p['actual_cost']) for p in projects)
    avg_completion = round(sum(float(p['completion_percentage']) for p in projects) / total_projects, 1) if total_projects else 0.0
    
    # 2. Material Stock Status & Valuation
    materials = conn.execute("SELECT * FROM materials").fetchall()
    total_materials_count = len(materials)
    low_stock_materials = [m for m in materials if m['current_stock'] <= m['min_threshold']]
    warehouse_valuation = sum(float(m['current_stock']) * float(m['unit_price']) for m in materials)
    
    # 3. Workforce & Attendance (Today)
    workers = conn.execute("SELECT * FROM workers").fetchall()
    total_workers = len(workers)
    active_workers = sum(1 for w in workers if w['status'] == 'Active')
    
    today_str = conn.execute("SELECT date('now')").fetchone()[0]
    today_attendance = conn.execute("SELECT * FROM attendance WHERE date = ?", (today_str,)).fetchall()
    if not today_attendance:
        # Check latest recorded attendance date
        latest_att_row = conn.execute("SELECT MAX(date) FROM attendance").fetchone()
        latest_date = latest_att_row[0] if latest_att_row and latest_att_row[0] else today_str
        today_attendance = conn.execute("SELECT * FROM attendance WHERE date = ?", (latest_date,)).fetchall()
        
    present_count = sum(1 for a in today_attendance if a['status'] == 'Present')
    daily_wages_sum = sum(float(a['daily_earning']) for a in today_attendance)
    
    # 4. Expenses Breakdown by Category
    expenses_by_cat = conn.execute("""
        SELECT expense_category, SUM(amount) as total
        FROM expenses
        GROUP BY expense_category
        ORDER BY total DESC;
    """).fetchall()
    
    expense_category_labels = [row['expense_category'] for row in expenses_by_cat]
    expense_category_values = [round(float(row['total']), 2) for row in expenses_by_cat]
    
    # 5. Recent Site Diary Entries
    diary_entries = conn.execute("""
        SELECT sd.*, p.name as project_name, u.full_name as author_name
        FROM site_diary sd
        JOIN projects p ON sd.project_id = p.id
        LEFT JOIN users u ON sd.logged_by_id = u.id
        ORDER BY sd.entry_date DESC
        LIMIT 5;
    """).fetchall()
    
    # 6. Recent Tasks
    recent_tasks = conn.execute("""
        SELECT t.*, p.name as project_name, u.full_name as assignee_name
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        LEFT JOIN users u ON t.assigned_to_id = u.id
        ORDER BY t.due_date ASC
        LIMIT 6;
    """).fetchall()
    
    # 7. Recent Enquiries (Leads)
    recent_leads = conn.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT 5").fetchall()
    
    conn.close()
    
    # Run ML Delay Risk Model on Active Projects
    delay_model = get_delay_model()
    project_risk_assessments = []
    
    for p in projects:
        if p['status'] in ('In Progress', 'Delayed'):
            # Calculate mock feature vector: [schedule_var, wf_rate, shortages, rain_days, crit_tasks]
            sched_var = 15.0 if p['status'] == 'Delayed' else 2.0
            wf_rate = 0.88
            shortages = len(low_stock_materials)
            rain_days = 1
            crit_tasks = 2
            
            risk_label = "Low"
            risk_badge = "success"
            if delay_model is not None:
                try:
                    feat = np.array([[sched_var, wf_rate, shortages, rain_days, crit_tasks]])
                    pred_class = delay_model.predict(feat)[0]
                    if pred_class == 1:
                        risk_label = "Moderate Risk"
                        risk_badge = "warning"
                    elif pred_class == 2:
                        risk_label = "High Delay Risk"
                        risk_badge = "danger"
                    else:
                        risk_label = "On Track"
                        risk_badge = "success"
                except Exception:
                    pass
            
            project_risk_assessments.append({
                "project_id": p['id'],
                "name": p['name'],
                "code": p['code'],
                "completion": p['completion_percentage'],
                "risk_label": risk_label,
                "risk_badge": risk_badge
            })

    return {
        "kpis": {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "delayed_projects": delayed_projects,
            "planning_projects": planning_projects,
            "avg_completion": avg_completion,
            "total_estimated_budget": total_estimated_budget,
            "total_actual_expenditure": total_actual_expenditure,
            "budget_spent_pct": round((total_actual_expenditure / total_estimated_budget * 100), 1) if total_estimated_budget else 0.0,
            "total_materials_count": total_materials_count,
            "low_stock_count": len(low_stock_materials),
            "warehouse_valuation": round(warehouse_valuation, 2),
            "total_workers": total_workers,
            "active_workers": active_workers,
            "present_workers_today": present_count,
            "attendance_rate": round((present_count / active_workers * 100), 1) if active_workers else 0.0,
            "daily_wages_sum": round(daily_wages_sum, 2)
        },
        "charts": {
            "project_status_labels": ["In Progress", "Completed", "Delayed", "Planning"],
            "project_status_counts": [active_projects, completed_projects, delayed_projects, planning_projects],
            "expense_labels": expense_category_labels,
            "expense_data": expense_category_values,
            "project_names": [p['name'][:18] + '...' for p in projects],
            "project_budgets": [p['budget'] / 100000.0 for p in projects], # In Lakhs
            "project_actuals": [p['actual_cost'] / 100000.0 for p in projects]
        },
        "low_stock_materials": [dict(m) for m in low_stock_materials],
        "project_risks": project_risk_assessments,
        "recent_diary": [dict(d) for d in diary_entries],
        "recent_tasks": [dict(t) for t in recent_tasks],
        "recent_leads": [dict(l) for l in recent_leads]
    }
