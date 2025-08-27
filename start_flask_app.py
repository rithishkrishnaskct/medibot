#!/usr/bin/env python3
"""
Startup script for Medical Drug Information Chatbot Flask Application
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """Check if the environment is properly set up"""
    logger.info("Checking environment setup...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        logger.warning(".env file not found. Creating from template...")
        env_example = Path('.env.example')
        if env_example.exists():
            import shutil
            shutil.copy('.env.example', '.env')
            logger.info("Created .env file from template. Please add your GOOGLE_API_KEY.")
        else:
            logger.error("No .env.example file found. Please create .env file manually.")
            return False
    
    # Check if required directories exist
    required_dirs = ['pdfs', 'uploads', 'vector_db', 'templates', 'static']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            logger.info(f"Creating directory: {dir_name}")
            dir_path.mkdir(exist_ok=True)
    
    return True

def install_dependencies():
    """Install required dependencies"""
    logger.info("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def start_flask_app():
    """Start the Flask application"""
    logger.info("Starting Medical Drug Information Chatbot Flask Application...")
    
    # Set environment variables
    os.environ.setdefault('FLASK_APP', 'flask_app.py')
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('HOST', '0.0.0.0')
    os.environ.setdefault('PORT', '12000')
    
    try:
        # Import and run the Flask app
        from flask_app import app, init_chatbot
        
        # Initialize chatbot
        init_chatbot()
        
        # Get configuration
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 12000))
        debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
        
        logger.info(f"Flask app starting on http://{host}:{port}")
        logger.info("Press Ctrl+C to stop the server")
        
        # Run the Flask app
        app.run(host=host, port=port, debug=debug)
        
    except ImportError as e:
        logger.error(f"Failed to import Flask app: {e}")
        logger.error("Make sure all dependencies are installed")
        return False
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("Medical Drug Information Chatbot - Flask Interface")
    logger.info("=" * 60)
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Dependency installation failed. Please check your Python environment.")
        sys.exit(1)
    
    # Start Flask app
    try:
        start_flask_app()
    except KeyboardInterrupt:
        logger.info("\nShutting down Flask application...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()