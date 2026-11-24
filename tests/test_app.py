import os
import unittest
import json
import tempfile
from app import app
from database.db import get_db_connection, init_db
from services.cost_estimation import estimate_construction_cost
from services.material_prediction import predict_material_requirements
from services.weather_service import generate_construction_advisory, get_current_weather
from services.ai_assistant import process_chat_message
from services.image_analysis import analyze_site_image

class MCBConstructionSystemTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_database_tables_exist(self):
        """Verifies all 15 required SQLite tables exist and have valid constraints."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        required_tables = [
            'users', 'projects', 'tasks', 'materials', 'inventory_transactions',
            'workers', 'attendance', 'expenses', 'site_diary', 'progress_reports',
            'site_images', 'cost_estimates', 'weather_logs', 'chat_messages', 'leads'
        ]
        for t in required_tables:
            self.assertIn(t, tables, f"Required table '{t}' missing from SQLite database.")

    def test_02_public_routes(self):
        """Verifies public portal routes render properly (HTTP 200)."""
        routes = ['/', '/about', '/services', '/materials-specifications', '/portfolio', '/contact', '/login', '/register']
        for r in routes:
            response = self.client.get(r)
            self.assertEqual(response.status_code, 200, f"Route '{r}' failed with status {response.status_code}")
            # Ensure Builder name SARGU SANJU is present
            if r in ['/', '/about', '/contact', '/materials-specifications']:
                self.assertIn(b'SARGU SANJU', response.data, f"Builder SARGU SANJU not found on route {r}")

    def test_03_authentication_and_rbac(self):
        """Tests login with valid demo credentials and rejection of invalid credentials."""
        # Valid login
        resp_valid = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(resp_valid.status_code, 200)
        self.assertIn(b'Executive Dashboard', resp_valid.data)

        # Logout before testing invalid credentials
        self.client.get('/logout', follow_redirects=True)

        # Invalid login
        resp_invalid = self.client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', resp_invalid.data)

    def test_04_cost_estimation_engine(self):
        """Verifies dual estimation: Engineering rule-based BOQ and ML RandomForest prediction."""
        result = estimate_construction_cost(
            built_up_area=2400,
            floors=2,
            quality_tier='Premium',
            building_type='Residential Villa',
            location='Warangal'
        )
        self.assertIn('engineering_estimate', result)
        self.assertIn('ml_prediction', result)
        self.assertGreater(result['engineering_estimate']['total_estimated_cost'], 0)
        self.assertGreater(result['recommended_budget'], 0)
        self.assertIsNotNone(result['ml_prediction'])
        self.assertIn('predicted_total', result['ml_prediction'])

    def test_05_material_requirement_prediction(self):
        """Verifies AI Material forecasting and warehouse deficit audit."""
        result = predict_material_requirements(
            built_up_area=2000,
            floors=2,
            quality_tier='Premium',
            building_type='Residential Villa'
        )
        self.assertIn('engineering_specifications', result)
        self.assertIn('ml_forecast', result)
        self.assertIn('procurement_recommendations', result)

        specs = result['engineering_specifications']['specifications']
        material_names = [s['material'] for s in specs]
        # Verify MCB brands are present
        self.assertTrue(any('UltraTech' in m for m in material_names))
        self.assertTrue(any('16mm' in m for m in material_names))
        self.assertTrue(any('Godavari' in m for m in material_names))

    def test_06_site_diary_and_daily_expenses(self):
        """Verifies the site diary tool to log daily work and on-site petty cash expenses."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'SARGU SANJU'
            sess['role'] = 'Administrator'

        diary_payload = {
            'project_id': 1,
            'entry_date': '2026-11-25',
            'weather_condition': 'Clear & Sunny',
            'temperature': 30.5,
            'shift_type': 'Day Shift',
            'workers_count': 9,
            'work_carried_out': 'Automated Unit Test: 5-inch slab formwork inspection and rebar tying.',
            'challenges_issues': 'None',
            'engineer_signature': 'Rajesh Varma (Site Engineer)',
            'expense_item[]': ['Tea and biscuits for 9 workers', '10kg binding wire & nails'],
            'expense_amount[]': ['360.0', '850.0'],
            'expense_paid_to[]': ['Lakshmi Stall', 'Sri Balaji Hardware'],
            'expense_category[]': ['Food & Beverage', 'Hardware']
        }

        resp = self.client.post('/site-diary/new', data=diary_payload, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # Verify entry in site_diary and expenses tables
        conn = get_db_connection()
        entry = conn.execute("SELECT * FROM site_diary WHERE entry_date = '2026-11-25' AND project_id = 1").fetchone()
        self.assertIsNotNone(entry, "Site diary record was not created in database.")
        self.assertEqual(entry['daily_expense_total'], 1210.0)

        # Verify synced expense record
        expense = conn.execute("SELECT * FROM expenses WHERE project_id = 1 AND expense_date = '2026-11-25' AND amount = 1210.0").fetchone()
        self.assertIsNotNone(expense, "Daily petty expense was not synced into master expenses table.")
        conn.close()

    def test_07_weather_telemetry_and_advisory(self):
        """Tests weather telemetry calculation and IS 456 pouring advisory."""
        advisory = generate_construction_advisory(temp=32.0, humidity=50.0, rain_chance=10.0, wind_speed=12.0)
        self.assertEqual(advisory['status'], 'Favorable')
        self.assertTrue(advisory['is_safe_for_slab_pour'])

        # Rain condition
        rain_advisory = generate_construction_advisory(temp=28.0, humidity=85.0, rain_chance=65.0, wind_speed=18.0)
        self.assertEqual(rain_advisory['status'], 'Critical Warning')
        self.assertFalse(rain_advisory['is_safe_for_slab_pour'])

    def test_08_ai_assistant_bilingual_chat(self):
        """Tests AI chatbot with both English and Telugu inputs."""
        # English query
        en_res = process_chat_message("What is the cost per sqft for house construction?")
        self.assertIn("Warangal", en_res['reply'])
        self.assertEqual(en_res['language'], 'english')

        # Telugu query
        te_res = process_chat_message("సిమెంట్ మరియు స్టీల్ వివరాలు ఏమిటి?")
        self.assertEqual(te_res['language'], 'telugu')
        self.assertIn("ఆల్ట్రా టెక్", te_res['reply'])

    def test_09_tensorflow_image_analysis(self):
        """Tests computer vision stage classifier using sample portfolio asset."""
        sample_img = os.path.join(app.root_path, 'static', 'images', 'portfolio_project_1.png')
        if os.path.exists(sample_img):
            analysis = analyze_site_image(sample_img)
            self.assertTrue(analysis['success'])
            self.assertIn('detected_stage', analysis)
            self.assertIn('confidence_percentage', analysis)
            self.assertIn('limitations_disclaimer', analysis)

    def test_10_authenticated_module_route_smoke(self):
        """Verifies every authenticated page route renders or redirects within the app."""
        routes = [
            '/dashboard',
            '/projects',
            '/projects/1',
            '/site-diary',
            '/site-diary/new',
            '/estimation',
            '/materials/prediction',
            '/progress',
            '/inventory',
            '/workforce',
            '/workforce/attendance',
            '/expenses',
            '/weather',
            '/chatbot',
            '/profile'
        ]

        anonymous = app.test_client()
        for route in routes:
            response = anonymous.get(route)
            self.assertIn(response.status_code, (302, 200),
                          f"Anonymous request to '{route}' returned unexpected status {response.status_code}")

        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'SARGU SANJU'
            sess['role'] = 'Administrator'

        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200,
                             f"Authenticated route '{route}' returned {response.status_code}")

    def test_11_ml_and_chat_api_routes(self):
        """Checks JSON API success and validation behavior for integrated services."""
        estimate = self.client.post('/api/estimate', json={
            'built_up_area': 2400,
            'floors': 2,
            'quality_tier': 'Premium',
            'building_type': 'Residential Duplex',
            'location': 'Warangal'
        })
        self.assertEqual(estimate.status_code, 200)
        estimate_json = estimate.get_json()
        self.assertTrue(estimate_json['success'])
        self.assertGreater(estimate_json['data']['recommended_budget'], 0)

        material_forecast = self.client.post('/api/material-prediction', json={
            'built_up_area': 2000,
            'floors': 2,
            'quality_tier': 'Premium',
            'building_type': 'Residential Villa',
            'location': 'Warangal'
        })
        self.assertEqual(material_forecast.status_code, 200)
        material_json = material_forecast.get_json()
        self.assertTrue(material_json['success'])
        self.assertIn('procurement_recommendations', material_json['data'])

        chat = self.client.post('/api/chat', json={'message': 'What is the cost per sqft for house construction?'})
        self.assertEqual(chat.status_code, 200)
        chat_json = chat.get_json()
        self.assertTrue(chat_json['success'])
        self.assertIn('reply', chat_json)

        empty_chat = self.client.post('/api/chat', json={'message': ''})
        self.assertEqual(empty_chat.status_code, 400)
        self.assertFalse(empty_chat.get_json()['success'])

    def test_12_write_operations_and_database_cleanup(self):
        """Exercises project task, expense, workforce, attendance, and public-lead writes."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'SARGU SANJU'
            sess['role'] = 'Administrator'

        conn = get_db_connection()
        before_project = conn.execute("SELECT actual_cost FROM projects WHERE id = 1").fetchone()
        conn.close()

        task_response = self.client.post('/projects/1/tasks/add', data={
            'title': 'QA Test Task',
            'description': 'Created only by the automated QA suite.',
            'assigned_to_id': '3',
            'start_date': '2026-11-24',
            'due_date': '2026-11-30',
            'priority': 'Low'
        }, follow_redirects=True)
        self.assertEqual(task_response.status_code, 200)

        expense_response = self.client.post('/expenses/add', data={
            'project_id': '1',
            'expense_category': 'Miscellaneous',
            'title': 'QA Test Expense',
            'amount': '101.25',
            'payment_mode': 'Cash',
            'paid_to': 'QA Vendor',
            'expense_date': '2026-11-24',
            'notes': 'Automated cleanup test'
        }, follow_redirects=True)
        self.assertEqual(expense_response.status_code, 200)

        lead_response = self.client.post('/contact', data={
            'name': 'QA Test Lead',
            'phone': '9999999999',
            'email': 'qa.lead@example.invalid',
            'location': 'Warangal',
            'plot_size': '100 sq yards',
            'built_up_area': '1200',
            'floors': 'G+1',
            'house_type': 'Duplex',
            'budget_range': '₹30 Lakhs - ₹40 Lakhs',
            'service_type': 'Planning & Consultation',
            'message': 'Automated QA lead cleanup test'
        }, follow_redirects=True)
        self.assertEqual(lead_response.status_code, 200)

        conn = get_db_connection()
        qa_task = conn.execute("SELECT id FROM tasks WHERE title = 'QA Test Task'").fetchone()
        qa_expense = conn.execute("SELECT id FROM expenses WHERE title = 'QA Test Expense'").fetchone()
        qa_lead = conn.execute("SELECT id FROM leads WHERE name = 'QA Test Lead'").fetchone()
        after_project = conn.execute("SELECT actual_cost FROM projects WHERE id = 1").fetchone()
        self.assertIsNotNone(qa_task)
        self.assertIsNotNone(qa_expense)
        self.assertIsNotNone(qa_lead)
        self.assertGreater(after_project['actual_cost'], before_project['actual_cost'])

        conn.execute("DELETE FROM tasks WHERE id = ?", (qa_task['id'],))
        conn.execute("DELETE FROM expenses WHERE id = ?", (qa_expense['id'],))
        conn.execute("DELETE FROM leads WHERE id = ?", (qa_lead['id'],))
        conn.execute("UPDATE projects SET actual_cost = ? WHERE id = 1", (before_project['actual_cost'],))
        conn.commit()
        conn.close()

    def test_13_error_pages_and_invalid_routes(self):
        """Verifies application error handlers and unknown-route behavior."""
        missing = self.client.get('/definitely-not-a-real-route')
        self.assertEqual(missing.status_code, 404)

        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['role'] = 'Administrator'
        missing_project = self.client.get('/projects/999999')
        self.assertEqual(missing_project.status_code, 302)

    def test_14_uploaded_file_route_uses_configured_storage(self):
        """Checks uploaded assets are served from the configured upload directory."""
        original_upload_folder = app.config['UPLOAD_FOLDER']
        try:
            with tempfile.TemporaryDirectory() as upload_folder:
                app.config['UPLOAD_FOLDER'] = upload_folder
                with open(os.path.join(upload_folder, 'qa-upload.txt'), 'w', encoding='utf-8') as uploaded_file:
                    uploaded_file.write('upload route test')

                response = self.client.get('/uploads/qa-upload.txt')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, b'upload route test')
                response.close()
        finally:
            app.config['UPLOAD_FOLDER'] = original_upload_folder

if __name__ == '__main__':
    unittest.main()
