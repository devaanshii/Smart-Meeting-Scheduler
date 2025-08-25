from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from meeting_agent import MeetingAgent

app = Flask(__name__)
CORS(app)

# Initialize database and agent
db = Database()
agent = MeetingAgent()

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all chat messages"""
    try:
        messages = db.get_messages()
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/messages', methods=['POST'])
def add_message():
    """Add a new message"""
    try:
        data = request.json
        db.add_message(data['user_name'], data['user_email'], data['message'])
        return jsonify({'success': True, 'message': 'Message added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/schedule-meeting', methods=['POST'])
def schedule_meeting():
    """Process chat and schedule meeting"""
    try:
        # Get all messages
        messages = db.get_messages()
        
        # Use AI agent to process
        result = agent.schedule_meeting(messages)
        
        if result['success'] and result['meeting_details']:
            # Save meeting to database
            meeting = result['meeting_details']
            db.save_meeting(
                meeting['title'],
                meeting['date'],
                meeting['time'],
                meeting['participants']
            )
            
            # Send confirmation emails
            agent.send_confirmation_email(meeting, meeting['participants'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = db.get_users()
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('index.htm', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "index.htm file not found. Make sure it's in the same directory as app.py", 404


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
