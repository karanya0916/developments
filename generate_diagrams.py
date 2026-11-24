import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('documentation/diagrams', exist_ok=True)
os.makedirs('documentation/screenshots', exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')

    # Title
    ax.text(6, 7.6, "MCB SMART CONSTRUCTION MANAGEMENT SYSTEM", fontsize=16, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6, 7.25, "Layered System Architecture & Multi-Agent Integration", fontsize=11, ha='center', color='#d97706', fontweight='semibold')

    # Presentation Layer (Frontend)
    p_box = patches.FancyBboxPatch((0.5, 5.5), 11, 1.3, boxstyle="round,pad=0.2", fc="#ffffff", ec="#0284c7", lw=2)
    ax.add_patch(p_box)
    ax.text(0.8, 6.5, "PRESENTATION LAYER (Frontend & Public Portal)", fontsize=11, fontweight='bold', color='#0369a1')
    ax.text(6, 6.0, "HTML5 • CSS3 Custom Architectural Theme • Bootstrap 5 • JavaScript • Chart.js Real-Time Telemetry\nBilingual Telugu (తెలుగు) & English Responsive UI • Photo Gallery • Interactive Sliders", fontsize=9.5, ha='center', color='#334155')

    # Application & API Layer (Flask Backend)
    a_box = patches.FancyBboxPatch((0.5, 3.6), 11, 1.5, boxstyle="round,pad=0.2", fc="#ffffff", ec="#ea580c", lw=2)
    ax.add_patch(a_box)
    ax.text(0.8, 4.8, "APPLICATION & BUSINESS LOGIC LAYER (Python Flask)", fontsize=11, fontweight='bold', color='#c2410c')
    modules_text = (
        "• Project Management & Task Velocity    • AI Cost Estimator (IS 456 BOQ)    • Material Forecast (Multi-Output)\n"
        "• Smart Material Inventory & GRN Logs   • Site Diary & Daily Expenses Tool  • Labour & Attendance Wages\n"
        "• Open-Meteo Weather Advisory Engine    • Bilingual Construction Chatbot    • RBAC Session Security"
    )
    ax.text(6, 4.15, modules_text, fontsize=9, ha='center', color='#1e293b')

    # AI, ML & Deep Learning Services
    ml_box = patches.FancyBboxPatch((0.5, 1.8), 5.3, 1.4, boxstyle="round,pad=0.2", fc="#ffffff", ec="#10b981", lw=2)
    ax.add_patch(ml_box)
    ax.text(0.7, 2.9, "AI & MACHINE LEARNING SERVICES", fontsize=10, fontweight='bold', color='#047857')
    ax.text(3.15, 2.3, "• Scikit-Learn Cost Regressor (R²=0.988)\n• MultiOutput Material Forecaster (R²=0.994)\n• GradientBoosting Project Delay Risk Classifier\n• NLP Rule-Based Bilingual Intent Engine", fontsize=8.5, ha='center', color='#334155')

    # Deep Learning (TensorFlow)
    dl_box = patches.FancyBboxPatch((6.2, 1.8), 5.3, 1.4, boxstyle="round,pad=0.2", fc="#ffffff", ec="#8b5cf6", lw=2)
    ax.add_patch(dl_box)
    ax.text(6.4, 2.9, "DEEP LEARNING COMPUTER VISION", fontsize=10, fontweight='bold', color='#6d28d9')
    ax.text(8.85, 2.3, "• TensorFlow/Keras Convolutional Neural Network\n• 3-Layer Conv2D + MaxPooling + Dense Dropout\n• Real-Time Construction Stage Classification\n• Foundation, Framing, Masonry, Finishing Detection", fontsize=8.5, ha='center', color='#334155')

    # Persistence Layer (SQLite Database)
    d_box = patches.FancyBboxPatch((0.5, 0.2), 11, 1.2, boxstyle="round,pad=0.2", fc="#0f172a", ec="#f59e0b", lw=2)
    ax.add_patch(d_box)
    ax.text(0.8, 1.1, "PERSISTENCE LAYER (SQLite Database - construction.db)", fontsize=11, fontweight='bold', color='#fbbf24')
    ax.text(6, 0.6, "15 Relational Tables: users • projects • tasks • materials • inventory_transactions • workers\nattendance • expenses • site_diary • progress_reports • site_images • cost_estimates • weather_logs • chat_messages • leads", fontsize=8.5, ha='center', color='#f8fafc')

    # Connecting Arrows
    ax.annotate('', xy=(6, 5.5), xytext=(6, 5.1), arrowprops=dict(arrowstyle="<->", color="#475569", lw=2))
    ax.annotate('', xy=(3.15, 3.6), xytext=(3.15, 3.2), arrowprops=dict(arrowstyle="<->", color="#475569", lw=2))
    ax.annotate('', xy=(8.85, 3.6), xytext=(8.85, 3.2), arrowprops=dict(arrowstyle="<->", color="#475569", lw=2))
    ax.annotate('', xy=(6, 1.8), xytext=(6, 1.4), arrowprops=dict(arrowstyle="<->", color="#475569", lw=2))

    plt.tight_layout()
    plt.savefig('documentation/diagrams/architecture_diagram.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/architecture_diagram.png")

def generate_dfd_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6, 6.6, "DATA FLOW DIAGRAM (LEVEL 0 & LEVEL 1)", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6, 6.25, "System Context & Core Information Flows", fontsize=10, ha='center', color='#d97706')

    # External Entities
    e1 = patches.FancyBboxPatch((0.5, 4.2), 2.2, 1.2, boxstyle="square,pad=0.1", fc="#f1f5f9", ec="#1e293b", lw=2)
    ax.add_patch(e1)
    ax.text(1.6, 4.8, "Client / Owner\n(Prospective Lead)", fontsize=9, fontweight='bold', ha='center', color='#0f172a')

    e2 = patches.FancyBboxPatch((0.5, 1.5), 2.2, 1.2, boxstyle="square,pad=0.1", fc="#f1f5f9", ec="#1e293b", lw=2)
    ax.add_patch(e2)
    ax.text(1.6, 2.1, "Site Engineer /\nSupervisor", fontsize=9, fontweight='bold', ha='center', color='#0f172a')

    e3 = patches.FancyBboxPatch((9.3, 4.2), 2.2, 1.2, boxstyle="square,pad=0.1", fc="#f1f5f9", ec="#1e293b", lw=2)
    ax.add_patch(e3)
    ax.text(10.4, 4.8, "Primary Builder\n(Sargu Sanju / Admin)", fontsize=9, fontweight='bold', ha='center', color='#0f172a')

    e4 = patches.FancyBboxPatch((9.3, 1.5), 2.2, 1.2, boxstyle="square,pad=0.1", fc="#f1f5f9", ec="#1e293b", lw=2)
    ax.add_patch(e4)
    ax.text(10.4, 2.1, "External Weather\nAPI (Open-Meteo)", fontsize=9, fontweight='bold', ha='center', color='#0f172a')

    # Central Process: MCB Management System
    p0 = patches.Circle((6, 3.5), 1.6, fc="#fff7ed", ec="#ea580c", lw=2.5)
    ax.add_patch(p0)
    ax.text(6, 3.7, "0.0\nMCB Construction\nManagement\nSystem", fontsize=10, fontweight='bold', ha='center', color='#9a3412')

    # Data Store
    ds = patches.FancyBboxPatch((4.5, 0.4), 3.0, 0.7, boxstyle="round,pad=0.1", fc="#0f172a", ec="#f59e0b", lw=1.5)
    ax.add_patch(ds)
    ax.text(6, 0.75, "D1: SQLite Database", fontsize=9, fontweight='bold', ha='center', color='#ffffff')

    # Flow arrows
    ax.annotate('Project Inquiry / Estimate Request', xy=(4.4, 4.2), xytext=(2.7, 4.8), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, color="#0369a1")
    ax.annotate('Daily Diary & Petty Cash / Photos', xy=(4.5, 3.0), xytext=(2.7, 2.1), arrowprops=dict(arrowstyle="->", color="#10b981", lw=1.5), fontsize=8, color="#047857")
    ax.annotate('Project Oversight & Approvals', xy=(7.6, 4.0), xytext=(9.3, 4.6), arrowprops=dict(arrowstyle="<-", color="#c2410c", lw=1.5), fontsize=8, color="#c2410c")
    ax.annotate('Live Weather Telemetry', xy=(7.5, 2.8), xytext=(9.3, 2.1), arrowprops=dict(arrowstyle="<-", color="#6d28d9", lw=1.5), fontsize=8, color="#6d28d9")
    ax.annotate('Store / Read Relational Data', xy=(6, 1.1), xytext=(6, 1.9), arrowprops=dict(arrowstyle="<->", color="#d97706", lw=1.5), fontsize=8, ha='center', color="#b45309")

    plt.tight_layout()
    plt.savefig('documentation/diagrams/dfd_level_0_1.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/dfd_level_0_1.png")

def generate_uml_diagrams():
    # Use Case Diagram
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(5, 5.6, "UML USE CASE DIAGRAM", fontsize=13, fontweight='bold', ha='center', color='#0f172a')

    # Actors
    ax.text(1.2, 4.5, "👤 Site Engineer", fontsize=10, fontweight='bold', ha='center', color='#0369a1')
    ax.text(1.2, 2.0, "👤 Primary Builder\n(Administrator)", fontsize=10, fontweight='bold', ha='center', color='#ea580c')

    # Use Cases (Ovals)
    cases = [
        ("Write Daily Site Diary & Petty Cash", 3.8, 4.8),
        ("Upload Site Image (AI Vision Stage)", 3.8, 3.8),
        ("Record Workforce Attendance & Wages", 3.8, 2.8),
        ("Run AI Cost & Material Estimation", 7.0, 4.8),
        ("Manage Material Inventory & Low Stock", 7.0, 3.8),
        ("Executive Analytics & Delay Risk Review", 7.0, 2.8),
        ("Consult Bilingual AI Chatbot Assistant", 5.4, 1.4)
    ]

    for title, x, y in cases:
        ellipse = patches.Ellipse((x, y), 2.6, 0.65, fc="#f8fafc", ec="#475569", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, title, fontsize=7.5, ha='center', va='center', color='#0f172a', fontweight='semibold')

    # Actor lines
    for title, x, y in cases[:3]:
        ax.plot([1.8, x - 1.3], [4.5, y], color="#94a3b8", lw=1.2, ls="--")
    for title, x, y in cases[3:6]:
        ax.plot([2.0, x - 1.3], [2.0, y], color="#94a3b8", lw=1.2, ls="--")
    ax.plot([2.0, 4.1], [2.0, 1.4], color="#94a3b8", lw=1.2, ls="--")

    plt.tight_layout()
    plt.savefig('documentation/diagrams/uml_usecase.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/uml_usecase.png")

    # ER Diagram
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6, 7.6, "ENTITY RELATIONSHIP (ER) DIAGRAM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6, 7.25, "Relational Schema & Foreign Key Mappings (SQLite)", fontsize=10, ha='center', color='#d97706')

    # Tables boxes
    tables = [
        ("USERS\nPK: id\nusername, email\npassword_hash\nrole, full_name, phone", 1.5, 5.5, "#dbeafe", "#1e40af"),
        ("PROJECTS\nPK: id\ncode, name, client\nplot_area, built_up\nfloors, budget, cost\nstatus, completion_%", 6.0, 5.5, "#ffedd5", "#c2410c"),
        ("TASKS\nPK: id\nFK: project_id\ntitle, description\nstart_date, due_date\npriority, status", 10.5, 5.5, "#f1f5f9", "#334155"),
        ("MATERIALS\nPK: id\nname, category, brand\ngrade_spec, unit\ncurrent_stock, min_thresh\nunit_price, supplier", 1.5, 2.2, "#dcfce7", "#15803d"),
        ("SITE_DIARY\nPK: id\nFK: project_id\nentry_date, shift\nwork_carried_out\npetty_expenses_json\ndaily_expense_total", 6.0, 2.2, "#fef3c7", "#b45309"),
        ("EXPENSES\nPK: id\nFK: project_id\ncategory, title\namount, payment_mode\npaid_to, receipt_no", 10.5, 2.2, "#fee2e2", "#b91c1c")
    ]

    for text, x, y, bg, border in tables:
        box = patches.FancyBboxPatch((x - 1.3, y - 1.1), 2.6, 2.2, boxstyle="round,pad=0.1", fc=bg, ec=border, lw=1.8)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=7.5, ha='center', va='center', color='#0f172a', fontweight='semibold')

    # Relationship connectors
    ax.plot([2.8, 4.7], [5.5, 5.5], color="#475569", lw=2)
    ax.text(3.75, 5.7, "1 : N (Manages)", fontsize=7.5, ha='center', color="#475569")

    ax.plot([7.3, 9.2], [5.5, 5.5], color="#475569", lw=2)
    ax.text(8.25, 5.7, "1 : N (Has Tasks)", fontsize=7.5, ha='center', color="#475569")

    ax.plot([6.0, 6.0], [4.4, 3.3], color="#475569", lw=2)
    ax.text(6.1, 3.85, "1 : N (Daily Log)", fontsize=7.5, ha='left', color="#475569")

    ax.plot([7.3, 9.2], [2.2, 2.2], color="#475569", lw=2)
    ax.text(8.25, 2.4, "Syncs Petty Exp", fontsize=7.5, ha='center', color="#475569")

    ax.plot([2.8, 4.7], [2.2, 2.2], color="#475569", lw=2)
    ax.text(3.75, 2.4, "Stock Issued", fontsize=7.5, ha='center', color="#475569")

    plt.tight_layout()
    plt.savefig('documentation/diagrams/er_diagram.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/er_diagram.png")

if __name__ == '__main__':
    generate_architecture_diagram()
    generate_dfd_diagram()
    generate_uml_diagrams()
