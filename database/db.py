import os
import sqlite3
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'construction.db')

if os.environ.get('VERCEL'):
    SOURCE_DB_PATH = DB_PATH
    DB_PATH = os.path.join('/tmp', 'construction.db')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH) and os.path.exists(SOURCE_DB_PATH):
        import shutil
        shutil.copy2(SOURCE_DB_PATH, DB_PATH)

def get_db_connection():
    """Returns an active SQLite connection configured with Row factory and foreign keys."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes all database tables with appropriate schemas, indexes, and initial seeds."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Administrator', 'Project Manager', 'Site Engineer', 'Inventory Manager')),
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        client_name TEXT NOT NULL,
        client_phone TEXT,
        location TEXT NOT NULL,
        building_type TEXT NOT NULL,
        plot_area REAL NOT NULL,
        built_up_area REAL NOT NULL,
        floors INTEGER NOT NULL DEFAULT 1,
        budget REAL NOT NULL,
        actual_cost REAL DEFAULT 0.0,
        start_date DATE NOT NULL,
        deadline DATE NOT NULL,
        status TEXT NOT NULL DEFAULT 'Planning' CHECK(status IN ('Planning', 'In Progress', 'Completed', 'Delayed', 'On Hold')),
        completion_percentage REAL DEFAULT 0.0,
        project_manager_id INTEGER,
        site_engineer_id INTEGER,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_manager_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (site_engineer_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 3. Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        assigned_to_id INTEGER,
        start_date DATE,
        due_date DATE,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'In Progress', 'Completed', 'Delayed')),
        priority TEXT NOT NULL DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
        completion_percentage REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (assigned_to_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 4. Materials Table (MCB Authentic Specifications)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        grade_spec TEXT,
        unit TEXT NOT NULL,
        current_stock REAL NOT NULL DEFAULT 0.0,
        min_threshold REAL NOT NULL DEFAULT 10.0,
        unit_price REAL NOT NULL DEFAULT 0.0,
        supplier_name TEXT,
        supplier_phone TEXT,
        location_in_site TEXT,
        is_mcb_approved INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Inventory Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        project_id INTEGER,
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('IN', 'OUT', 'WASTAGE', 'RETURN')),
        quantity REAL NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        reference_no TEXT,
        logged_by_id INTEGER,
        notes TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
        FOREIGN KEY (logged_by_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 6. Workers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        skill_category TEXT NOT NULL CHECK(skill_category IN ('Mason', 'Steel Fixer', 'Carpenter', 'Plumber', 'Electrician', 'Painter', 'General Labor', 'Site Supervisor')),
        daily_wage_rate REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'On Leave', 'Inactive')),
        aadhar_id TEXT,
        emergency_contact TEXT,
        joined_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status TEXT NOT NULL DEFAULT 'Present' CHECK(status IN ('Present', 'Absent', 'Half Day')),
        hours_worked REAL DEFAULT 8.0,
        overtime_hours REAL DEFAULT 0.0,
        daily_earning REAL NOT NULL DEFAULT 0.0,
        recorded_by_id INTEGER,
        notes TEXT,
        FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (recorded_by_id) REFERENCES users(id) ON DELETE SET NULL,
        UNIQUE(worker_id, project_id, date)
    );
    """)

    # 8. Expenses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        expense_category TEXT NOT NULL CHECK(expense_category IN ('Material', 'Labour', 'Equipment', 'Subcontract', 'Fuel & Transport', 'Permits & Approvals', 'Petty Cash', 'Miscellaneous')),
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_mode TEXT NOT NULL DEFAULT 'Cash' CHECK(payment_mode IN ('Cash', 'UPI/Online', 'Bank Transfer', 'Cheque')),
        paid_to TEXT,
        receipt_number TEXT,
        receipt_image TEXT,
        expense_date DATE NOT NULL,
        approved_by_id INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (approved_by_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 9. Site Diary Table (Site activity & daily expense diary)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        entry_date DATE NOT NULL,
        weather_condition TEXT,
        temperature REAL,
        shift_type TEXT DEFAULT 'Day Shift',
        work_carried_out TEXT NOT NULL,
        challenges_issues TEXT,
        workers_count INTEGER DEFAULT 0,
        daily_expense_total REAL DEFAULT 0.0,
        petty_expenses_json TEXT, -- JSON array of [{item, amount, paid_to, category}]
        photos_json TEXT,          -- JSON array of photo file paths
        logged_by_id INTEGER,
        engineer_signature TEXT,
        verified_by_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (logged_by_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (verified_by_id) REFERENCES users(id) ON DELETE SET NULL,
        UNIQUE(project_id, entry_date, shift_type)
    );
    """)

    # 10. Progress Reports Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        report_date DATE NOT NULL,
        milestone_name TEXT NOT NULL,
        planned_percentage REAL NOT NULL,
        actual_percentage REAL NOT NULL,
        variance_percentage REAL NOT NULL,
        activities_completed TEXT,
        pending_activities TEXT,
        delay_reasons TEXT,
        corrective_action TEXT,
        submitted_by_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (submitted_by_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 11. Site Images Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        thumbnail_path TEXT,
        stage_category TEXT NOT NULL CHECK(stage_category IN ('Foundation', 'RCC_Framing', 'Masonry', 'Plastering', 'Finishing', 'Safety_Issue', 'Exterior')),
        ai_detected_stage TEXT,
        ai_confidence REAL,
        inspection_status TEXT DEFAULT 'Pending' CHECK(inspection_status IN ('Pending', 'Approved', 'Flagged')),
        notes TEXT,
        uploaded_by_id INTEGER,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (uploaded_by_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 12. Cost Estimates Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_estimates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        client_name TEXT NOT NULL,
        building_type TEXT NOT NULL,
        plot_area REAL NOT NULL,
        built_up_area REAL NOT NULL,
        floors INTEGER NOT NULL,
        quality_tier TEXT NOT NULL CHECK(quality_tier IN ('Standard', 'Premium', 'Luxury')),
        location TEXT NOT NULL,
        estimated_total_cost REAL NOT NULL,
        civil_cost REAL NOT NULL,
        finishing_cost REAL NOT NULL,
        mep_cost REAL NOT NULL,
        labour_cost REAL NOT NULL,
        material_breakdown_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
    );
    """)

    # 13. Weather Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        recorded_date DATE NOT NULL,
        location TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        rainfall_chance REAL,
        wind_speed REAL,
        condition_text TEXT,
        advisory TEXT,
        cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 14. Chat Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
        message TEXT NOT NULL,
        intent TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 15. Leads Table (Public Inquiry Portal)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        location TEXT NOT NULL,
        plot_size TEXT,
        built_up_area REAL,
        floors TEXT,
        house_type TEXT,
        budget_range TEXT,
        service_type TEXT,
        message TEXT,
        status TEXT DEFAULT 'New' CHECK(status IN ('New', 'Contacted', 'Site Visit Scheduled', 'Estimate Sent', 'Won', 'Lost')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create Indexes for Query Performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_project ON expenses(project_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_worker ON attendance(worker_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_diary_project_date ON site_diary(project_id, entry_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_material ON inventory_transactions(material_id);")

    conn.commit()
    conn.close()
    print("Database tables initialized successfully with indexes and constraints.")

if __name__ == '__main__':
    init_db()
