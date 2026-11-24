# MCB Website - QA and System Validation Report

**Validation date:** 24 November 2026  
**Environment:** Windows, Python 3.12.10, Flask 3.1.9  
**Server verification:** `http://127.0.0.1:5000/` returned HTTP 200

## Automated Test Result

Command: `python -m unittest discover -s tests -v`

**Result:** 13 tests executed, 13 passed, 0 failed.

| Test | Actual Result |
|---|---|
| `test_01_database_tables_exist` | PASS - 15 required tables verified |
| `test_02_public_routes` | PASS - Public routes returned HTTP 200 |
| `test_03_authentication_and_rbac` | PASS - Valid and invalid authentication verified |
| `test_04_cost_estimation_engine` | PASS - Engineering and ML cost outputs verified |
| `test_05_material_requirement_prediction` | PASS - Engineering and ML material outputs verified |
| `test_06_site_diary_and_daily_expenses` | PASS - Diary-to-expense synchronization verified |
| `test_07_weather_telemetry_and_advisory` | PASS - Favorable and critical advisory branches verified |
| `test_08_ai_assistant_bilingual_chat` | PASS - English and Telugu responses verified |
| `test_09_tensorflow_image_analysis` | PASS - CNN model loaded and analysis completed |
| `test_10_authenticated_module_route_smoke` | PASS - Protected modules rendered and anonymous access redirected |
| `test_11_ml_and_chat_api_routes` | PASS - Estimation, material, and chat APIs verified |
| `test_12_write_operations_and_database_cleanup` | PASS - Test writes verified and cleaned |
| `test_13_error_pages_and_invalid_routes` | PASS - 404 and missing-project behavior verified |

## Live Application Verification

- Landing page rendered successfully.
- Administrator login succeeded and the executive dashboard rendered.
- Live weather telemetry used the Open-Meteo Live API during browser validation.
- Project, inventory, diary, progress, chatbot, workforce, expense, and weather pages loaded in the running browser.
- Actual browser screenshots are stored in `documentation/screenshots/` with `_actual.png` names.

## Validated ML Integrations

- Scikit-Learn cost estimator loaded and returned a positive recommended budget.
- Scikit-Learn material forecaster returned procurement recommendations.
- TensorFlow/Keras construction-stage classifier loaded and completed sample image analysis.
- Bilingual chatbot English and Telugu paths returned verified responses.
- Open-Meteo weather API was reached live; documented fallback logic remains available for offline use.

## Known Limitations

- TensorFlow output is an assistive construction-stage tag, not a certified inspection.
- Cost and material forecasts require qualified engineering review.
- Development server and demo credentials are not production security controls.
