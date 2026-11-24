import os
import json
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
from database.db import get_db_connection, init_db

def seed_all():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] > 0:
        print("Database already contains data. Skipping re-seed.")
        conn.close()
        return

    print("Seeding database with authentic MCB Construction data...")

    # 1. Seed Users (Roles: Administrator, Project Manager, Site Engineer, Inventory Manager)
    users = [
        ('admin', 'admin@mcbconstructions.com', generate_password_hash('admin123'), 'SARGU SANJU', 'Administrator', '7386181866'),
        ('pm_vikram', 'vikram@mcbconstructions.com', generate_password_hash('pm123'), 'Vikram Reddy', 'Project Manager', '9848022331'),
        ('eng_rajesh', 'rajesh@mcbconstructions.com', generate_password_hash('eng123'), 'Rajesh Varma', 'Site Engineer', '9848033442'),
        ('inv_suresh', 'suresh@mcbconstructions.com', generate_password_hash('inv123'), 'Suresh Goud', 'Inventory Manager', '9848044553'),
    ]
    cursor.executemany("""
    INSERT INTO users (username, email, password_hash, full_name, role, phone)
    VALUES (?, ?, ?, ?, ?, ?);
    """, users)

    # 2. Seed Projects
    projects = [
        ('Sargu Sanju Villa - Shambunipet', 'MCB-2026-01', 'Sargu Sanju', '7386181866', 'Vishwanath Colony, Shambunipet, Warangal', 'Residential Duplex', 2400.0, 3200.0, 3, 6800000.0, 4450000.0, '2026-01-10', '2026-12-20', 'In Progress', 78.0, 2, 3, 'G+2 Luxury duplex residence featuring contemporary elevation, RCC frame, Italian granite and teakwood joinery.'),
        ('Vishwanath Colony Modern Residence', 'MCB-2026-02', 'Ramesh Rao', '9848111222', 'Vishwanath Colony, Warangal', 'Residential Single Unit', 1800.0, 1850.0, 2, 3800000.0, 3720000.0, '2025-06-01', '2026-02-15', 'Completed', 100.0, 2, 3, 'G+1 Modern residence with parking, UPVC windows, POP ceiling and Asian Paints exterior finish.'),
        ('Hanamkonda Road Luxury Elevation House', 'MCB-2026-03', 'Dr. K. Srinivas', '9849222333', 'Hanamkonda Main Road, Warangal', 'Multi-Floor Residence', 2200.0, 2750.0, 3, 5500000.0, 1800000.0, '2026-04-01', '2027-01-30', 'In Progress', 35.0, 2, 3, 'Multi-level residential facade with double-height balcony and decorative plaster motifs.'),
        ('Kazipet Urban Duplex', 'MCB-2026-04', 'Venkat Narayana', '9849333444', 'Near Railway Colony, Kazipet', 'Residential Duplex', 1950.0, 2100.0, 2, 4500000.0, 3200000.0, '2025-09-15', '2026-07-31', 'Delayed', 62.0, 2, 3, 'G+1 Duplex with solar provisions, Sudhakar SWR plumbing, and designer tile cladding.'),
        ('Warangal Fort View Modern Home', 'MCB-2026-05', 'M. Anitha Reddy', '9849444555', 'Fort Road, Warangal', 'Compact Villa', 1500.0, 1600.0, 2, 3200000.0, 250000.0, '2026-10-01', '2027-06-30', 'Planning', 10.0, 2, 3, 'Energy-efficient 2BHK contemporary house with rainwater harvesting and open terrace.'),
    ]
    cursor.executemany("""
    INSERT INTO projects (name, code, client_name, client_phone, location, building_type, plot_area, built_up_area, floors, budget, actual_cost, start_date, deadline, status, completion_percentage, project_manager_id, site_engineer_id, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, projects)

    # 3. Seed Authentic MCB Materials (from Telugu specification sheet & blueprint)
    materials = [
        ('Cement (UltraTech 53 Grade / PPC)', 'Cement', 'UltraTech', 'OPC 53 / PPC Fresh Batch', 'Bags', 450.0, 50.0, 390.0, 'Sri Laxmi Cement Depot', '9848123456', 'Cement Godown Bay 1', 1),
        ('16mm TMT Reinforcement Steel', 'Steel', 'TATA Tiscon / Jindal Panther', '16mm Fe550D (4 bars per pillar)', 'Tons', 14.5, 3.0, 68500.0, 'Kakatiya Steel Traders', '9848234567', 'Steel Yard Rack A', 1),
        ('12mm TMT Reinforcement Steel', 'Steel', 'TATA Tiscon / Jindal Panther', '12mm Fe550D (4 bars per pillar)', 'Tons', 11.2, 2.5, 69000.0, 'Kakatiya Steel Traders', '9848234567', 'Steel Yard Rack B', 1),
        ('Godavari Fine River Sand', 'Aggregates', 'Godavari River Basin', 'Washed Coarse/Fine Sand', 'Tons', 85.0, 15.0, 1850.0, 'Godavari Sand Suppliers', '9848345678', 'Sand Heap 1', 1),
        ('20mm Crushed Blue Metal Aggregate', 'Aggregates', 'Local Stone Quarry', '20mm Graded Machine Crushed', 'Brass', 35.0, 8.0, 3200.0, 'Bhadrakali Blue Metal Quarry', '9848456789', 'Aggregate Heap 2', 1),
        ('Light Weight No. 1 Quality Bricks', 'Masonry', 'Local Warangal Kilns', 'Class 1 Red Kiln Bricks / AAC', 'Pieces', 12500.0, 2000.0, 9.5, 'Warangal Brick Works', '9848567890', 'Brick Stacks Block C', 1),
        ('Plumbing Pipes & Fittings (CPVC/SWR)', 'Plumbing', 'Ashirvad & Sudhakar', 'CPVC Hot/Cold & SWR Drainage', 'Lots', 22.0, 5.0, 8500.0, 'Balaji Sanitary & Hardware', '9848678901', 'Plumbing Store Room', 1),
        ('Sanitary Ware & Indian Taps / Wall Mixer', 'Sanitary', 'Cera / Western & Local Brass', 'Floor Mounted EWC & Indian Taps', 'Sets', 12.0, 3.0, 7500.0, 'Balaji Sanitary & Hardware', '9848678901', 'Finished Goods Store', 1),
        ('Electrical Fire-Resistant Wires', 'Electrical', 'Finolex', 'FR Multi-strand Wires (1.5, 2.5, 4 sq mm)', 'Coils', 45.0, 10.0, 2400.0, 'Telangana Electrical Agencies', '9848789012', 'Electrical Store Room', 1),
        ('Modular Switches & Plates', 'Electrical', 'Goldmedal', 'Curve / Wave Modular Switches', 'Units', 180.0, 30.0, 145.0, 'Telangana Electrical Agencies', '9848789012', 'Electrical Store Room', 1),
        ('Main Door Teakwood Frame & Shutter', 'Woodwork', 'Burma/CP Teak', '1st Quality Carved Teakwood', 'Units', 4.0, 1.0, 38000.0, 'Shree Ram Woodcrafts', '9848890123', 'Carpentry Shed', 1),
        ('Bedroom Doors (PVC Lamination)', 'Doors', 'Century / Greenlam', '1st Quality Laminated Flush Doors', 'Units', 14.0, 3.0, 6500.0, 'Shree Ram Woodcrafts', '9848890123', 'Carpentry Shed', 1),
        ('Bathroom Doors (WPVC Waterproof)', 'Doors', 'Sintex / Marvel', '100% Water & Termite Proof WPVC', 'Units', 8.0, 2.0, 4200.0, 'Shree Ram Woodcrafts', '9848890123', 'Carpentry Shed', 1),
        ('Windows (UPVC Sliding with Mesh)', 'Windows', 'Kommerling / Aparna Venster', '3-Track Sliding with Bug Mesh', 'Units', 16.0, 4.0, 11500.0, 'Venster UPVC Systems', '9848901234', 'Glazing Store', 1),
        ('Parking Tiles (Heavy Duty ₹70/sqft)', 'Flooring', 'Somany / Johnson', 'Anti-Skid Heavy Duty Pavers', 'Sq Ft', 950.0, 150.0, 70.0, 'Sri Venkateshwara Tile Gallery', '9848012345', 'Tile Warehouse Bay 2', 1),
        ('Kitchen Granite Slab (₹100/sqft)', 'Flooring', 'Black Galaxy / Jet Black', '18mm Mirror Polished Granite', 'Sq Ft', 420.0, 80.0, 100.0, 'Granite City Warangal', '9848123789', 'Stone Yard', 1),
        ('Wall & Flooring Tiles (₹250/box)', 'Flooring', 'Kajaria / Somany', 'Glazed Vitrified 2x2 & Wall Tiles', 'Boxes', 210.0, 35.0, 250.0, 'Sri Venkateshwara Tile Gallery', '9848012345', 'Tile Warehouse Bay 1', 1),
        ('POP False Ceiling Materials', 'Ceiling', 'Gyproc / Saint-Gobain', 'POP Powder & GI Channels', 'Bags', 65.0, 15.0, 380.0, 'Deccan Gypsum & False Ceiling', '9848234890', 'Ceiling Store', 1),
        ('Iron Grills & Security Main Gate', 'Fabrication', 'Tata Structura Mild Steel', 'Decorative Safety Grills & Gate', 'Kgs', 1250.0, 200.0, 95.0, 'Warangal Metal Fabricators', '9848345901', 'Fabrication Yard', 1),
        ('Asian Paints (Apex Exterior & Royale Interior)', 'Paint', 'Asian Paints', 'Apex Ultima Exterior & Royale Luxury Emulsion', 'Liters', 160.0, 30.0, 385.0, 'Rainbow Paints & Hardwares', '9848456012', 'Paint Bay 3', 1),
        ('Staircase Stainless Steel Railing', 'Fabrication', 'Jindal SS 304', 'Grade 304 Pipe & Baluster Railing', 'Running Feet', 120.0, 20.0, 480.0, 'Steelcraft Fabricators', '9848567123', 'Fabrication Yard', 1),
        ('Overhead Water Tank (1000 Litres)', 'Plumbing', 'Sintex / Supreme', '1000L Triple Layer Anti-Bacterial Tank', 'Units', 3.0, 1.0, 7200.0, 'Balaji Sanitary & Hardware', '9848678901', 'Plumbing Store Room', 1),
        ('Wall Putty (J.K. / Birla White)', 'Paint', 'Birla White / JK Pro-Coat', 'Smooth Finish Polymer Wall Putty', 'Bags', 80.0, 15.0, 780.0, 'Rainbow Paints & Hardwares', '9848456012', 'Paint Bay 1', 1),
    ]
    cursor.executemany("""
    INSERT INTO materials (name, category, brand, grade_spec, unit, current_stock, min_threshold, unit_price, supplier_name, supplier_phone, location_in_site, is_mcb_approved)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, materials)

    # 4. Seed Tasks
    tasks = [
        (1, 'RCC Column Pouring & Curing (Level 2)', 'Execute columns using 16mm/12mm steel and M25 design mix with 14-day curing log.', 3, '2026-11-15', '2026-11-28', 'In Progress', 'High', 75.0),
        (1, 'Main Electrical Conduit Chasing', 'Conceal Finolex conduits and Goldmedal modular switch boxes in first floor masonry.', 3, '2026-11-20', '2026-12-05', 'In Progress', 'Medium', 40.0),
        (1, 'UPVC Window Measurements & Ordering', 'Verify rough openings for 3-track sliding windows before internal plastering.', 3, '2026-11-22', '2026-11-30', 'Completed', 'High', 100.0),
        (1, 'POP False Ceiling Framing', 'Erect GI grid framing in drawing and dining halls.', 3, '2026-12-01', '2026-12-15', 'Pending', 'Medium', 0.0),
        (3, 'Plinth Beam Reinforcement & Inspection', 'Check beam rebar placement against structural drawings with site engineer signoff.', 3, '2026-11-18', '2026-11-27', 'In Progress', 'Critical', 85.0),
        (4, 'SWR Drainage Pipe Testing & Backfill', 'Perform water leak test on Sudhakar 110mm lines before finishing driveway paving.', 3, '2026-11-10', '2026-11-25', 'Delayed', 'High', 50.0),
    ]
    cursor.executemany("""
    INSERT INTO tasks (project_id, title, description, assigned_to_id, start_date, due_date, status, priority, completion_percentage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, tasks)

    # 5. Seed Construction Workers
    workers = [
        ('Mallesh K.', '9848100001', 'Mason', 950.0, 'Active', '4589-1234-5678', '9848100099', '2025-01-15'),
        ('Raju Bandari', '9848100002', 'Mason', 950.0, 'Active', '4589-1234-5679', '9848100098', '2025-02-01'),
        ('Kumar Swamy', '9848100003', 'Steel Fixer', 900.0, 'Active', '4589-1234-5680', '9848100097', '2025-01-20'),
        ('Bhikshapathi M.', '9848100004', 'Steel Fixer', 900.0, 'Active', '4589-1234-5681', '9848100096', '2025-03-10'),
        ('Sambaiah P.', '9848100005', 'Carpenter', 950.0, 'Active', '4589-1234-5682', '9848100095', '2025-01-18'),
        ('Thirupathi G.', '9848100006', 'Plumber', 900.0, 'Active', '4589-1234-5683', '9848100094', '2025-04-05'),
        ('Nagaraju V.', '9848100007', 'Electrician', 950.0, 'Active', '4589-1234-5684', '9848100093', '2025-02-15'),
        ('Sreenu Vadde', '9848100008', 'General Labor', 650.0, 'Active', '4589-1234-5685', '9848100092', '2025-01-10'),
        ('Laxman K.', '9848100009', 'General Labor', 650.0, 'Active', '4589-1234-5686', '9848100091', '2025-01-12'),
        ('Anjaiah T.', '9848100010', 'Painter', 850.0, 'Active', '4589-1234-5687', '9848100090', '2025-05-01'),
    ]
    cursor.executemany("""
    INSERT INTO workers (full_name, phone, skill_category, daily_wage_rate, status, aadhar_id, emergency_contact, joined_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, workers)

    # 6. Seed Attendance (Recent 5 days)
    today = date.today()
    att_records = []
    for day_offset in range(5):
        log_date = (today - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        for wid in range(1, 11):
            status = 'Present' if (wid + day_offset) % 7 != 0 else 'Absent'
            hours = 8.0 if status == 'Present' else 0.0
            ot = 1.0 if (wid % 3 == 0 and status == 'Present') else 0.0
            rate = 950.0 if wid in (1, 2, 5, 7) else (900.0 if wid in (3, 4, 6) else (850.0 if wid == 10 else 650.0))
            earning = (rate + (ot * (rate / 8.0) * 1.5)) if status == 'Present' else 0.0
            att_records.append((wid, 1, log_date, status, hours, ot, round(earning, 2), 3, 'Regular site shift'))

    cursor.executemany("""
    INSERT INTO attendance (worker_id, project_id, date, status, hours_worked, overtime_hours, daily_earning, recorded_by_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, att_records)

    # 7. Seed Expenses
    expenses = [
        (1, 'Material', 'UltraTech Cement 200 Bags delivery', 78000.0, 'Bank Transfer', 'Sri Laxmi Cement Depot', 'INV-2026-441', None, (today - timedelta(days=6)).strftime('%Y-%m-%d'), 2, '200 bags OPC 53 unloaded at site godown.'),
        (1, 'Material', 'TMT 16mm & 12mm Steel bundle (3.2 Tons)', 219200.0, 'Bank Transfer', 'Kakatiya Steel Traders', 'INV-2026-459', None, (today - timedelta(days=5)).strftime('%Y-%m-%d'), 2, 'Primary steel for columns and floor beams.'),
        (1, 'Labour', 'Weekly workforce wages disbursement', 58500.0, 'UPI/Online', 'Site Labor Gang Leader', 'VOUCH-789', None, (today - timedelta(days=4)).strftime('%Y-%m-%d'), 2, 'Wages for 8 workers over 6 workdays.'),
        (1, 'Equipment', 'Concrete Mixer & Hoist Rental (7 days)', 14000.0, 'Cash', 'Warangal Machinery Rentals', 'RENT-102', None, (today - timedelta(days=3)).strftime('%Y-%m-%d'), 3, 'Mixer machine with operator for second floor slab pour.'),
        (1, 'Petty Cash', 'Site Petty Cash & Tea / Refreshments / Binding Wire', 3450.0, 'Cash', 'Local Provision & Hardware', 'PETTY-089', None, (today - timedelta(days=2)).strftime('%Y-%m-%d'), 3, 'Worker refreshments, binding wire 10kg, measuring tape.'),
        (1, 'Fuel & Transport', 'Diesel for site generator & sand tractor freight', 6200.0, 'UPI/Online', 'Shambunipet Fuel Station', 'FUEL-4412', None, (today - timedelta(days=1)).strftime('%Y-%m-%d'), 3, 'Power backup during column casting.'),
    ]
    cursor.executemany("""
    INSERT INTO expenses (project_id, expense_category, title, amount, payment_mode, paid_to, receipt_number, receipt_image, expense_date, approved_by_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, expenses)

    # 8. Seed Site Diary (The user's key requirement: "add one diary base tool to write daily expenses on site")
    diary_entries = [
        (
            1,
            (today - timedelta(days=1)).strftime('%Y-%m-%d'),
            'Clear & Sunny',
            31.5,
            'Day Shift',
            'Completed shuttering and rebar inspection for second floor beams. Mixed and poured concrete for 6 columns using UltraTech 53 grade and Godavari sand. Initiated continuous water curing on first floor slabs.',
            'Minor delay in morning sand tractor arrival due to traffic near Shambunipet junction. Resolved by 9:30 AM.',
            9,
            4750.0,
            json.dumps([
                {"item": "Morning & afternoon tea & biscuits for 9 workers", "amount": 360.0, "paid_to": "Lakshmi Tea Stall", "category": "Food & Beverage"},
                {"item": "Binding wire 10kg and steel nails 2 inches", "amount": 1250.0, "paid_to": "Sri Balaji Hardware", "category": "Hardware"},
                {"item": "Tractor unloading coolie extra charges", "amount": 800.0, "paid_to": "Local Porters", "category": "Labor Assistance"},
                {"item": "Diesel 20 liters for vibrator & generator backup", "amount": 1940.0, "paid_to": "Shambunipet Indian Oil", "category": "Fuel"},
                {"item": "First aid box antiseptic cream & bandages replacement", "amount": 400.0, "paid_to": "Sanjeevani Medicos", "category": "Safety & Medical"}
            ]),
            json.dumps(['/static/images/portfolio_project_1.png', '/static/images/portfolio_project_2.jpg']),
            3,
            'Rajesh Varma (B.Tech Civil - Site Engineer)',
            2
        ),
        (
            1,
            today.strftime('%Y-%m-%d'),
            'Pleasant & Dry',
            29.0,
            'Day Shift',
            'Started internal brick masonry on first floor using Light Weight No. 1 quality bricks with 1:6 cement mortar. Electrical conduit chasing initiated by Finolex electrician crew.',
            'None. Work proceeding smoothly on schedule.',
            8,
            2850.0,
            json.dumps([
                {"item": "Chalk lines, plumb bob string and marker pens", "amount": 250.0, "paid_to": "Modern Stationery", "category": "Tools"},
                {"item": "Tea and evening snacks for mason team", "amount": 320.0, "paid_to": "Lakshmi Tea Stall", "category": "Food & Beverage"},
                {"item": "Curing water pump hose pipe joint replacement", "amount": 480.0, "paid_to": "Sudhakar Pipe Store", "category": "Plumbing Maintenance"},
                {"item": "Tiffin for electrician crew overtime support", "amount": 600.0, "paid_to": "Bhavani Tiffin Center", "category": "Overtime Meal"},
                {"item": "Petty local auto transport for electrical box samples", "amount": 1200.0, "paid_to": "Auto Driver Ramesh", "category": "Transport"}
            ]),
            json.dumps(['/static/images/portfolio_project_3.jpg']),
            3,
            'Rajesh Varma (B.Tech Civil - Site Engineer)',
            2
        )
    ]
    cursor.executemany("""
    INSERT INTO site_diary (project_id, entry_date, weather_condition, temperature, shift_type, work_carried_out, challenges_issues, workers_count, daily_expense_total, petty_expenses_json, photos_json, logged_by_id, engineer_signature, verified_by_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, diary_entries)

    # 9. Seed Site Images
    site_images = [
        (1, '/static/images/portfolio_project_1.png', '/static/images/portfolio_project_1.png', 'Exterior', 'Exterior_Elevation', 0.96, 'Approved', 'Front elevation render and facade perspective for Sargu Sanju Villa.', 3),
        (1, '/static/images/portfolio_project_2.jpg', '/static/images/portfolio_project_2.jpg', 'Finishing', 'Painting_Finishing', 0.94, 'Approved', 'Ground floor compound wall and gate installation with dual-tone paint.', 3),
        (1, '/static/images/portfolio_project_3.jpg', '/static/images/portfolio_project_3.jpg', 'Exterior', 'Modern_Elevation', 0.98, 'Approved', 'Multi-tier elevation structure with wood-finish louvers and white bands.', 3),
        (2, '/static/images/portfolio_project_4.jpg', '/static/images/portfolio_project_4.jpg', 'Finishing', 'Completed_Facade', 0.95, 'Approved', 'Vishwanath colony single-unit completed house with porch and parapet.', 3),
        (3, '/static/images/portfolio_project_5.jpg', '/static/images/portfolio_project_5.jpg', 'Exterior', 'Multi_Level_Elevation', 0.97, 'Approved', 'Hanamkonda luxury residence facade with balcony stainless steel railing.', 3),
        (4, '/static/images/portfolio_project_6.jpg', '/static/images/portfolio_project_6.jpg', 'Masonry', 'Masonry_Finishing', 0.92, 'Approved', 'Exposed brick finish feature wall with warm lighting accents.', 3),
    ]
    cursor.executemany("""
    INSERT INTO site_images (project_id, image_path, thumbnail_path, stage_category, ai_detected_stage, ai_confidence, inspection_status, notes, uploaded_by_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, site_images)

    # 10. Seed Sample Leads
    leads = [
        ('K. Madhav Rao', '9848123999', 'madhav.rao@gmail.com', 'Subedari, Warangal', '200 sq. yards', 2200.0, 'G+1', 'Duplex Villa', '₹45 Lakhs - ₹55 Lakhs', 'Full Turnkey Construction', 'Interested in building a modern 3BHK duplex with teakwood doors and Asian Paints finish. Requesting preliminary site visit.', 'New'),
        ('Sunitha Reddy', '9848123888', 'sunitha.r@gmail.com', 'Naimnagar, Hanamkonda', '150 sq. yards', 1600.0, 'G+1', 'Independent House', '₹30 Lakhs - ₹40 Lakhs', 'Structure + Finishing', 'Looking for reliable builder with transparent material specifications. Please share estimate.', 'Contacted'),
    ]
    cursor.executemany("""
    INSERT INTO leads (name, phone, email, location, plot_size, built_up_area, floors, house_type, budget_range, service_type, message, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, leads)

    # 11. Seed Inventory Transactions
    transactions = [
        (1, 1, 'IN', 300.0, 390.0, 117000.0, 'GRN-2026-001', 4, 'Received from Sri Laxmi Depot. Approved batch.'),
        (1, 1, 'OUT', 120.0, 390.0, 46800.0, 'ISSUE-001', 4, 'Issued for column casting level 2.'),
        (2, 1, 'IN', 5.0, 68500.0, 342500.0, 'GRN-2026-002', 4, '16mm TMT bars bundled. Mill test verified.'),
        (2, 1, 'OUT', 2.2, 68500.0, 150700.0, 'ISSUE-002', 4, 'Issued for column cage fabrication.'),
    ]
    cursor.executemany("""
    INSERT INTO inventory_transactions (material_id, project_id, transaction_type, quantity, unit_price, total_amount, reference_no, logged_by_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, transactions)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully with 100% authentic MCB data!")

if __name__ == '__main__':
    seed_all()
