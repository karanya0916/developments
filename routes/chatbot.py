import uuid
from flask import Blueprint, render_template, request, jsonify, session
from services.ai_assistant import process_chat_message
from database.db import get_db_connection

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot')
def index():
    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())

    # Load recent chat history
    conn = get_db_connection()
    messages = conn.execute("""
        SELECT * FROM chat_messages 
        WHERE session_id = ? 
        ORDER BY timestamp ASC 
        LIMIT 20
    """, (session['chat_session_id'],)).fetchall()
    conn.close()

    return render_template('chatbot.html', messages=messages)

@chatbot_bp.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    user_msg = data.get('message', '').strip()

    if not user_msg:
        return jsonify({"success": False, "error": "Message is empty."}), 400

    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())

    sess_id = session['chat_session_id']
    user_id = session.get('user_id')

    result = process_chat_message(user_msg, session_id=sess_id, user_id=user_id)
    return jsonify({
        "success": True,
        "reply": result['reply'],
        "intent": result['intent'],
        "language": result['language'],
        "timestamp": result['timestamp']
    })
