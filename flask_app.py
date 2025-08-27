#!/usr/bin/env python3
"""
Flask Web Application for Medical Drug Information Chatbot
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import logging
from datetime import datetime

# Import our existing chatbot components
from chatbot import MedicalChatbot
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'medical-chatbot-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize chatbot
chatbot = None

def init_chatbot():
    """Initialize the chatbot instance"""
    global chatbot
    try:
        chatbot = MedicalChatbot()
        logger.info("Medical chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        chatbot = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@app.route('/')
def index():
    """Main chat interface"""
    session_id = get_session_id()
    return render_template('index.html', session_id=session_id)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if not chatbot:
            return jsonify({
                'error': 'Chatbot not initialized. Please check your configuration.',
                'response': 'I apologize, but the medical chatbot is currently unavailable. Please try again later.'
            }), 500

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        session_id = get_session_id()
        
        # Get response from chatbot
        response = chatbot.get_response(user_message, session_id)
        
        # Log the interaction
        logger.info(f"Session {session_id}: User: {user_message[:100]}...")
        logger.info(f"Session {session_id}: Bot: {response[:100]}...")
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while processing your message.',
            'response': 'I apologize, but I encountered an error while processing your request. Please try again.'
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF file uploads"""
    try:
        if not chatbot:
            return jsonify({'error': 'Chatbot not initialized'}), 500

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)
            
            # Process the uploaded PDF
            success = chatbot.add_pdf(filepath)
            
            if success:
                return jsonify({
                    'message': f'Successfully uploaded and processed {file.filename}',
                    'filename': filename
                })
            else:
                # Clean up failed upload
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': 'Failed to process the PDF file'}), 500
        else:
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        return jsonify({'error': 'An error occurred while uploading the file'}), 500

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear current session"""
    try:
        session_id = get_session_id()
        if chatbot:
            chatbot.clear_session(session_id)
        
        # Generate new session ID
        session['session_id'] = str(uuid.uuid4())
        
        return jsonify({
            'message': 'Session cleared successfully',
            'new_session_id': session['session_id']
        })
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        return jsonify({'error': 'Failed to clear session'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy' if chatbot else 'unhealthy',
        'chatbot_initialized': chatbot is not None,
        'timestamp': datetime.now().isoformat()
    }
    
    if chatbot:
        try:
            # Test basic functionality
            test_response = chatbot.get_response("test", "health_check")
            status['chatbot_responsive'] = True
        except:
            status['chatbot_responsive'] = False
            status['status'] = 'degraded'
    
    return jsonify(status)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize chatbot
    init_chatbot()
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 12000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on {host}:{port}")
    app.run(host=host, port=port, debug=debug)