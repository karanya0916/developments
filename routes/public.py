from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database.db import get_db_connection

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang

    conn = get_db_connection()
    materials = conn.execute("SELECT * FROM materials ORDER BY category ASC LIMIT 16").fetchall()
    conn.close()

    portfolio_projects = [
        {
            "id": 1,
            "title_en": "Sargu Sanju Luxury Villa",
            "title_te": "సర్గూ సంజు లగ్జరీ విల్లా",
            "location": "Vishwanath Colony, Shambunipet, Warangal",
            "type": "G+2 Contemporary Duplex",
            "built_up": "3,200 sq.ft",
            "image": "/static/images/portfolio_project_1.png",
            "badge": "Flagship Project"
        },
        {
            "id": 2,
            "title_en": "Modern G+1 Compact Residence",
            "title_te": "ఆధునిక కాంపాక్ట్ హౌస్",
            "location": "Vishwanath Colony, Warangal",
            "type": "G+1 Residential Unit",
            "built_up": "1,850 sq.ft",
            "image": "/static/images/portfolio_project_2.jpg",
            "badge": "Completed"
        },
        {
            "id": 3,
            "title_en": "Multi-Level Residential Facade",
            "title_te": "బహుళ అంతస్తుల నివాస భవనం",
            "location": "Hanamkonda Main Road, Warangal",
            "type": "G+2 Contemporary Villa",
            "built_up": "2,750 sq.ft",
            "image": "/static/images/portfolio_project_3.jpg",
            "badge": "Ongoing"
        },
        {
            "id": 4,
            "title_en": "Contemporary Front Elevation",
            "title_te": "ఆధునిక ఫ్రంట్ ఎలివేషన్",
            "location": "Kazipet Urban Area",
            "type": "G+1 Independent House",
            "built_up": "2,100 sq.ft",
            "image": "/static/images/portfolio_project_4.jpg",
            "badge": "Delivered"
        },
        {
            "id": 5,
            "title_en": "Multi-Tier Designer Residence",
            "title_te": "ప్రీమియం నివాస భవనం",
            "location": "Fort Road, Warangal",
            "type": "G+2 Multi-level Unit",
            "built_up": "2,600 sq.ft",
            "image": "/static/images/portfolio_project_5.jpg",
            "badge": "Featured"
        },
        {
            "id": 6,
            "title_en": "Warm Accent Brick Elevation",
            "title_te": "ఇటుక ఎలివేషన్ డిజైన్",
            "location": "Subedari, Warangal",
            "type": "G+1 Duplex House",
            "built_up": "1,950 sq.ft",
            "image": "/static/images/portfolio_project_6.jpg",
            "badge": "Completed"
        },
        {
            "id": 7,
            "title_en": "Contemporary 2-Storey Residence",
            "title_te": "ఆధునిక 2 అంతస్తుల ఇల్లు",
            "location": "Naimnagar, Hanamkonda",
            "type": "G+1 Contemporary Villa",
            "built_up": "2,300 sq.ft",
            "image": "/static/images/portfolio_project_7.jpg",
            "badge": "Delivered"
        },
        {
            "id": 8,
            "title_en": "Premium Luxury Elevation Concept",
            "title_te": "ప్రీమియం నివాస ఎలివేషన్",
            "location": "Shambunipet, Warangal",
            "type": "G+2 Designer House",
            "built_up": "3,100 sq.ft",
            "image": "/static/images/portfolio_project_8.jpg",
            "badge": "Under Construction"
        }
    ]

    return render_template(
        'public/index.html',
        lang=lang,
        portfolio_projects=portfolio_projects,
        materials=materials
    )

@public_bp.route('/about')
def about():
    lang = request.args.get('lang', session.get('lang', 'en'))
    return render_template('public/about.html', lang=lang)

@public_bp.route('/services')
def services_page():
    lang = request.args.get('lang', session.get('lang', 'en'))
    return render_template('public/services.html', lang=lang)

@public_bp.route('/materials-specifications')
def materials_specifications():
    lang = request.args.get('lang', session.get('lang', 'en'))
    conn = get_db_connection()
    materials = conn.execute("SELECT * FROM materials ORDER BY category ASC").fetchall()
    conn.close()
    return render_template('public/materials.html', materials=materials, lang=lang)

@public_bp.route('/portfolio')
def portfolio():
    lang = request.args.get('lang', session.get('lang', 'en'))
    return render_template('public/portfolio.html', lang=lang)

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', session.get('lang', 'en'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        location = request.form.get('location', '').strip()
        plot_size = request.form.get('plot_size', '').strip()
        built_up_area = float(request.form.get('built_up_area', 0.0) or 0.0)
        floors = request.form.get('floors', 'G+1')
        house_type = request.form.get('house_type', 'Duplex Villa')
        budget_range = request.form.get('budget_range', '₹35 Lakhs - ₹50 Lakhs')
        service_type = request.form.get('service_type', 'Full Turnkey Construction')
        message = request.form.get('message', '').strip()

        if not name or not phone:
            flash('Please provide your name and phone number so builder Sargu Sanju can contact you.', 'danger')
            return render_template('public/contact.html', lang=lang)

        conn = get_db_connection()
        conn.execute("""
        INSERT INTO leads (name, phone, email, location, plot_size, built_up_area, floors, house_type, budget_range, service_type, message, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'New');
        """, (name, phone, email, location, plot_size, built_up_area, floors, house_type, budget_range, service_type, message))
        conn.commit()
        conn.close()

        msg = "ధన్యవాదాలు! మీ విచారణ నమోదు చేయబడింది. బిల్డర్ సర్గూ సంజు మిమ్మల్ని త్వరలో సంప్రదిస్తారు." if lang == 'te' else "Thank you! Your construction inquiry has been received. Builder Sargu Sanju will contact you shortly."
        flash(msg, 'success')
        return redirect(url_for('public.contact', lang=lang))

    return render_template('public/contact.html', lang=lang)
