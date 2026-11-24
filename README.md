# MCB Smart Construction Management System

Professional Flask and SQLite construction management portal for Mamatha Constructions & Builders (MCB), Warangal.

## Features

- Public bilingual portal in English and Telugu
- Role-based authentication and project management
- Construction cost estimation with rule-based BOQ and Scikit-Learn prediction
- Material quantity forecasting and inventory stock auditing
- Site diary, daily petty-cash expenses, and photo evidence
- Workforce registration and attendance/wage calculations
- Progress reports and TensorFlow/Keras construction-stage image classification
- Open-Meteo live weather and IS 456-style construction advisories
- Bilingual knowledge-base chatbot
- Executive dashboard, charts, project risks, and expense summaries

## Requirements

- Windows 10/11 or another supported Python environment
- Python 3.12 recommended
- Internet access is optional for live weather; the system has a fallback weather source

## Installation

```powershell
cd "C:\Users\sargu_3niengw\OneDrive\Desktop\MCB Website"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install flask werkzeug numpy joblib scikit-learn pandas requests pillow tensorflow python-docx reportlab matplotlib
```

`train_models.py` may be run once to regenerate the local Scikit-Learn models:

```powershell
python train_models.py
```

## Initialize and Run

The SQLite schema is initialized automatically from `database/db.py` when the application starts.

```powershell
python app.py
```

Open `http://127.0.0.1:5000/`.

## Demo Accounts

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `admin123` |
| Project Manager | `pm_vikram` | `pm123` |
| Site Engineer | `eng_rajesh` | `eng123` |
| Inventory Manager | `inv_suresh` | `inv123` |

## Automated Testing

Run the complete unittest suite:

```powershell
python -m unittest discover -s tests -v
```

The expanded suite covers database schema, public routes, authentication, cost and material models, weather advisory, bilingual chat, TensorFlow image analysis, all authenticated route smoke checks, JSON APIs, write operations, cleanup, and 404 handling.

## Documentation

Generated project documentation and evidence are stored in `documentation/`:

- `MCB_Project_Documentation.docx`
- `MCB_Project_Documentation.pdf`
- `QA_Test_Report.md`
- `screenshots/`
- `diagrams/`

## Project Structure

```text
app.py                  Flask application and blueprint registration
config.py               Environment and application configuration
routes/                 Flask route blueprints
services/               Estimation, forecasting, weather, chat, and vision services
database/db.py          SQLite schema and connection management
database/seed_data.py   Demonstration data seeding
ml_models/              Trained cost, material, delay, and vision models
templates/              Jinja HTML templates
static/                 CSS, JavaScript, images, and uploads
tests/test_app.py       Automated unittest suite
documentation/          Screenshots, diagrams, QA report, DOCX, and PDF
```

## Notes

- Do not commit real credentials or production API keys to source control.
- The TensorFlow stage classifier is an assistive indexing feature and does not replace certified structural inspection.
- ML outputs are estimates and should be verified by a qualified engineer for procurement or construction decisions.
