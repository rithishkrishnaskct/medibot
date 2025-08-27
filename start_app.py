#!/usr/bin/env python3
"""
Startup script for the Medical Drug Information Chatbot
"""
import subprocess
import sys
import os

def main():
    """Start the Streamlit application"""
    print("🏥 Starting Medical Drug Information Chatbot...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the medibot directory.")
        sys.exit(1)
    
    # Check if sample PDFs exist
    if not os.path.exists("pdfs"):
        print("📄 Creating pdfs directory...")
        os.makedirs("pdfs", exist_ok=True)
    
    # Create sample PDFs if they don't exist
    if not os.listdir("pdfs"):
        print("📄 Creating sample medical PDFs...")
        try:
            subprocess.run([sys.executable, "create_sample_pdf.py"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  Could not create sample PDFs. You can add your own PDFs to the pdfs/ directory.")
    
    print("\n🚀 Starting Streamlit application...")
    print("📱 The application will be available at: http://localhost:12000")
    print("🔑 Don't forget to enter your Google Gemini API key in the sidebar!")
    print("\n" + "=" * 50)
    
    # Start Streamlit
    try:
        subprocess.run([
            "streamlit", "run", "app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "12000",
            "--server.headless", "true"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Medical Chatbot...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()