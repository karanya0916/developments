from datetime import datetime
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle


PROJECT_DIR = Path(__file__).resolve().parents[1]
DOC_DIR = PROJECT_DIR / "documentation"
SCREENSHOT_DIR = DOC_DIR / "screenshots"
DIAGRAM_DIR = DOC_DIR / "diagrams"

TESTS = [
    ("test_01_database_tables_exist", "15 required SQLite tables verified"),
    ("test_02_public_routes", "Public and public/portal routes returned HTTP 200"),
    ("test_03_authentication_and_rbac", "Valid login, invalid login, and dashboard authorization verified"),
    ("test_04_cost_estimation_engine", "Engineering and RandomForest cost estimates verified"),
    ("test_05_material_requirement_prediction", "Engineering BOQ and ML material forecast verified"),
    ("test_06_site_diary_and_daily_expenses", "Diary and master expense synchronization verified"),
    ("test_07_weather_telemetry_and_advisory", "Weather safety and pouring advisory verified"),
    ("test_08_ai_assistant_bilingual_chat", "English and Telugu assistant responses verified"),
    ("test_09_tensorflow_image_analysis", "TensorFlow CNN image analysis verified"),
    ("test_10_authenticated_module_route_smoke", "Authenticated modules and anonymous redirects verified"),
    ("test_11_ml_and_chat_api_routes", "Estimation, material, and chat JSON APIs verified"),
    ("test_12_write_operations_and_database_cleanup", "Project task, expense, and lead writes verified and cleaned"),
    ("test_13_error_pages_and_invalid_routes", "404 handling and missing-project redirect verified"),
]


def add_docx_heading(document, text, level=1):
    document.add_heading(text, level=level)


def generate_docx():
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("MAMATHA CONSTRUCTIONS & BUILDERS")
    run.bold = True
    run.font.size = Pt(22)
    subtitle = document.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle.add_run("MCB Smart Construction Management System")
    subtitle_run.bold = True
    subtitle_run.font.size = Pt(16)
    date_run = document.add_paragraph()
    date_run.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_run.add_run("Project Documentation and QA Validation\n24 November 2026")

    add_docx_heading(document, "1. Executive Summary", 1)
    document.add_paragraph(
        "The MCB Smart Construction Management System is a Flask/SQLite construction operations "
        "portal for residential project management in Warangal and Telangana. It combines public "
        "lead capture, role-based administration, engineering estimation, inventory, workforce, "
        "site diary, progress image analysis, weather telemetry, and bilingual assistance."
    )

    add_docx_heading(document, "2. Scope and Completed Modules", 1)
    modules = [
        "Public portal and Telugu/English language support",
        "Authentication and role-based access control",
        "Executive dashboard and project analytics",
        "Project, task, expense, and site-diary management",
        "Inventory, attendance, workforce, and payroll calculations",
        "Engineering cost BOQ and Scikit-Learn cost prediction",
        "Material forecasting and warehouse deficiency auditing",
        "TensorFlow/Keras construction-stage image classification",
        "Open-Meteo live weather and construction advisory",
        "Bilingual construction chatbot and SQLite chat history",
    ]
    for module in modules:
        document.add_paragraph(module, style="List Bullet")

    add_docx_heading(document, "3. Technology Stack", 1)
    technology = [
        ("Presentation", "HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js"),
        ("Application", "Python 3.12, Flask blueprints"),
        ("Data", "SQLite 15-table relational schema"),
        ("ML", "Scikit-Learn cost/material/delay models"),
        ("Computer Vision", "TensorFlow/Keras Convolutional Neural Network"),
        ("External Integration", "Open-Meteo weather API"),
    ]
    table = document.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.rows[0].cells[0].text = "Layer"
    table.rows[0].cells[1].text = "Implementation"
    for layer, implementation in technology:
        row = table.add_row().cells
        row[0].text = layer
        row[1].text = implementation

    add_docx_heading(document, "4. System Architecture", 1)
    architecture = DIAGRAM_DIR / "architecture_diagram.png"
    if architecture.exists():
        document.add_picture(str(architecture), width=Inches(6.7))
        document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_docx_heading(document, "5. Data Flow and Data Model", 1)
    for name in ("dfd_level_0_1.png", "er_diagram.png"):
        path = DIAGRAM_DIR / name
        if path.exists():
            document.add_picture(str(path), width=Inches(6.7))
            document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_docx_heading(document, "6. UML Diagrams", 1)
    for name in (
        "uml_usecase.png",
        "uml_class_diagram.png",
        "uml_activity_diagram.png",
        "uml_sequence_diagram.png",
    ):
        path = DIAGRAM_DIR / name
        if path.exists():
            document.add_picture(str(path), width=Inches(6.7))
            document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_docx_heading(document, "7. Installation and Execution", 1)
    document.add_paragraph(
        "Create a virtual environment, install Flask and ML dependencies, then run python app.py "
        "from the project directory. Open http://127.0.0.1:5000/ in a browser."
    )
    document.add_paragraph(
        "Demo administrator credentials: admin / admin123. Additional demo accounts are documented "
        "in README.md."
    )

    add_docx_heading(document, "8. Testing and QA Results", 1)
    document.add_paragraph(
        "Validation command: python -m unittest discover -s tests -v"
    )
    document.add_paragraph("13 tests executed; 13 passed; 0 failed.")
    test_table = document.add_table(rows=1, cols=3)
    test_table.style = "Table Grid"
    test_table.rows[0].cells[0].text = "Test"
    test_table.rows[0].cells[1].text = "Result"
    test_table.rows[0].cells[2].text = "Evidence"
    for test_name, evidence in TESTS:
        row = test_table.add_row().cells
        row[0].text = test_name
        row[1].text = "PASS"
        row[2].text = evidence

    add_docx_heading(document, "9. Live Application Screenshots", 1)
    screenshot_names = [
        ("01_public_landing_page_actual.png", "Public landing page"),
        ("02_executive_admin_dashboard_actual.png", "Executive dashboard"),
        ("03_ai_cost_estimator_actual.png", "AI cost estimator"),
        ("04_material_inventory_actual.png", "Material inventory"),
        ("05_projects_actual.png", "Project management"),
        ("06_site_diary_daily_expenses_actual.png", "Site diary"),
        ("07_progress_tensorflow_vision_actual.png", "Progress and TensorFlow vision"),
        ("08_bilingual_ai_chatbot_actual.png", "Bilingual chatbot"),
        ("09_workforce_actual.png", "Workforce"),
        ("10_expenses_actual.png", "Expense ledger"),
        ("11_weather_actual.png", "Weather telemetry"),
    ]
    for filename, caption in screenshot_names:
        path = SCREENSHOT_DIR / filename
        if path.exists():
            add_docx_heading(document, caption, 2)
            document.add_picture(str(path), width=Inches(6.7))
            document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_docx_heading(document, "10. Limitations and Production Readiness", 1)
    document.add_paragraph(
        "The TensorFlow image stage classifier assists photo tagging and is not a substitute for "
        "certified structural inspection or laboratory strength testing. ML cost and material "
        "estimates must be reviewed by a qualified engineer before procurement or construction "
        "commitments. A production deployment should replace the development secret key, isolate "
        "the database, restrict file uploads, configure HTTPS, and add server-side CSRF protection."
    )

    output = DOC_DIR / "MCB_Project_Documentation.docx"
    document.save(output)
    return output


def generate_pdf():
    output = DOC_DIR / "MCB_Project_Documentation.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8))

    def page_header(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.55 * inch, 0.35 * inch, "MCB Smart Construction Management System")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = [
        Paragraph("MAMATHA CONSTRUCTIONS & BUILDERS", styles["Title"]),
        Paragraph("MCB Smart Construction Management System", styles["Heading1"]),
        Paragraph("Project Documentation and QA Validation", styles["Heading2"]),
        Paragraph("24 November 2026", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("1. Executive Summary", styles["Heading1"]),
        Paragraph(
            "The MCB system is a Flask/SQLite construction operations portal for projects in Warangal "
            "and Telangana. It provides public leads, role-based administration, project and expense "
            "management, material and cost tools, workforce operations, weather integration, and "
            "bilingual assistance.",
            styles["Normal"],
        ),
        Paragraph("2. Scope and Completed Modules", styles["Heading1"]),
    ]
    for module in [
        "Public bilingual portal",
        "Authentication and role-based access",
        "Executive dashboard and project analytics",
        "Project, task, diary, attendance, inventory, and expense operations",
        "Engineering and ML cost/material models",
        "TensorFlow construction image analysis",
        "Open-Meteo weather telemetry",
        "Bilingual chatbot",
    ]:
        story.append(Paragraph("• " + module, styles["Normal"]))

    story += [Paragraph("3. System Architecture", styles["Heading1"])]
    for name in ("architecture_diagram.png", "dfd_level_0_1.png", "er_diagram.png",
                 "uml_usecase.png", "uml_class_diagram.png", "uml_activity_diagram.png",
                 "uml_sequence_diagram.png"):
        path = DIAGRAM_DIR / name
        if path.exists():
            story.append(Image(str(path), width=7.2 * inch, height=4.1 * inch))
            story.append(Spacer(1, 8))

    story += [PageBreak(), Paragraph("4. Testing and QA Results", styles["Heading1"]),
              Paragraph("Command: python -m unittest discover -s tests -v", styles["Normal"]),
              Paragraph("13 tests executed; 13 passed; 0 failed.", styles["Normal"])]
    table_data = [["Test", "Result", "Evidence"]]
    table_data += [[name, "PASS", evidence] for name, evidence in TESTS]
    table = Table(table_data, colWidths=[2.0 * inch, 0.55 * inch, 4.45 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    story += [PageBreak(), Paragraph("5. Live Application Screenshots", styles["Heading1"])]
    for filename, caption in [
        ("01_public_landing_page_actual.png", "Public landing page"),
        ("02_executive_admin_dashboard_actual.png", "Executive dashboard"),
        ("03_ai_cost_estimator_actual.png", "AI cost estimator"),
        ("04_material_inventory_actual.png", "Material inventory"),
        ("05_projects_actual.png", "Project management"),
        ("06_site_diary_daily_expenses_actual.png", "Site diary"),
        ("07_progress_tensorflow_vision_actual.png", "Progress and TensorFlow vision"),
        ("08_bilingual_ai_chatbot_actual.png", "Bilingual chatbot"),
        ("09_workforce_actual.png", "Workforce"),
        ("10_expenses_actual.png", "Expense ledger"),
        ("11_weather_actual.png", "Weather telemetry"),
    ]:
        path = SCREENSHOT_DIR / filename
        if path.exists():
            story.append(Paragraph(caption, styles["Heading2"]))
            story.append(Image(str(path), width=7.2 * inch, height=4.5 * inch))
            story.append(Spacer(1, 10))

    story += [
        PageBreak(),
        Paragraph("6. Installation and Execution", styles["Heading1"]),
        Paragraph("Create a virtual environment and install the required packages.", styles["Normal"]),
        Paragraph("python -m pip install flask werkzeug numpy joblib scikit-learn requests pillow tensorflow python-docx reportlab matplotlib", styles["Code"]),
        Paragraph("python app.py", styles["Code"]),
        Paragraph("Open http://127.0.0.1:5000/", styles["Normal"]),
        Paragraph("7. Limitations", styles["Heading1"]),
        Paragraph(
            "TensorFlow vision, cost, material, and delay estimates are assistive outputs and require "
            "qualified engineering review. Production deployment requires HTTPS, secure secret "
            "configuration, database isolation, upload restrictions, and CSRF protection.",
            styles["Normal"],
        ),
    ]

    doc.build(story, onFirstPage=page_header, onLaterPages=page_header)
    return output


if __name__ == "__main__":
    docx_output = generate_docx()
    pdf_output = generate_pdf()
    print(docx_output)
    print(pdf_output)
