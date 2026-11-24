import os
import sys
import traceback

from flask import Flask, jsonify

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('VERCEL', '1')

try:
    from app import app as flask_app
except Exception as startup_error:
    startup_trace = traceback.format_exc()
    flask_app = Flask(__name__)

    @flask_app.route('/', defaults={'path': ''})
    @flask_app.route('/<path:path>')
    def startup_error_response(path):
        return jsonify({
            'success': False,
            'error': 'MCB application startup failed.',
            'exception': str(startup_error),
            'traceback': startup_trace
        }), 500


# Vercel Python functions and local WSGI servers both recognize these exports.
app = flask_app
handler = flask_app
