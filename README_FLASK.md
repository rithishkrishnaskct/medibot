# Medical Drug Information Chatbot - Flask Interface

A comprehensive Flask-based web application for medical drug information queries using RAG (Retrieval-Augmented Generation) with Google's Gemini API.

## 🏥 Features

### Core Functionality
- **Medical-focused Q&A**: Answers only medical and drug-related questions
- **PDF Document Processing**: Upload and analyze drug information PDFs
- **Contextual Conversations**: Maintains session-based conversation history
- **Citation Support**: Provides source references from uploaded documents
- **Real-time Chat Interface**: Modern, responsive web interface

### Technical Features
- **RAG Implementation**: Uses sentence transformers and FAISS for document retrieval
- **Session Management**: Maintains conversation context per user session
- **File Upload**: Secure PDF upload with validation (max 16MB)
- **Health Monitoring**: Built-in health check endpoints
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Required Python packages (see requirements.txt)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rithishkrishnaskct/medibot.git
   cd medibot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   ```

4. **Start the Flask application**:
   ```bash
   python flask_app.py
   ```
   
   Or use the startup script:
   ```bash
   python start_flask_app.py
   ```

5. **Access the application**:
   - Open your browser and go to: `http://localhost:12000`
   - Or use the provided runtime URL if running in a hosted environment

## 🖥️ Interface Overview

### Main Chat Interface
- **Left Sidebar**: 
  - PDF upload functionality
  - Session management controls
  - Quick question examples
  - Session information display

- **Main Chat Area**:
  - Real-time conversation interface
  - Message history with timestamps
  - Typing indicators
  - Citation display for referenced documents

- **Input Area**:
  - Text input for questions
  - Send button with loading states
  - Medical context validation

### Key UI Components
- **Responsive Design**: Works on desktop and mobile devices
- **Bootstrap 5**: Modern, professional styling
- **Font Awesome Icons**: Intuitive visual elements
- **Real-time Feedback**: Loading states, progress indicators, and notifications

## 📁 Project Structure

```
medibot/
├── flask_app.py              # Main Flask application
├── start_flask_app.py        # Startup script with environment checks
├── chatbot.py                # Core chatbot logic
├── pdf_processor.py          # PDF processing and RAG implementation
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Main chat interface
│   ├── 404.html             # Error page
│   └── 500.html             # Server error page
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css        # Custom styling
│   └── js/
│       └── app.js           # Frontend JavaScript
├── pdfs/                     # Sample PDF documents
├── uploads/                  # User uploaded files
└── vector_db/               # FAISS vector database
```

## 🔧 API Endpoints

### Main Routes
- `GET /` - Main chat interface
- `POST /chat` - Send chat messages
- `POST /upload` - Upload PDF files
- `POST /clear_session` - Clear conversation history
- `GET /health` - Health check endpoint

### Example API Usage

**Send a chat message**:
```bash
curl -X POST http://localhost:12000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the dosage for Humira?"}'
```

**Upload a PDF**:
```bash
curl -X POST http://localhost:12000/upload \
  -F "file=@drug_info.pdf"
```

**Health check**:
```bash
curl http://localhost:12000/health
```

## ⚙️ Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `FLASK_SECRET_KEY`: Flask session secret key (optional, defaults to development key)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 12000)
- `FLASK_DEBUG`: Enable debug mode (default: False)

### Application Settings
- **Max file size**: 16MB for PDF uploads
- **Allowed file types**: PDF only
- **Session timeout**: Configurable in Flask session settings
- **Vector database**: FAISS with sentence transformers

## 🔒 Security Features

- **File validation**: Only PDF files allowed
- **File size limits**: Maximum 16MB uploads
- **Secure filenames**: Uses werkzeug secure_filename
- **Session management**: UUID-based session IDs
- **Input sanitization**: Validates and sanitizes user inputs
- **Medical context filtering**: Only responds to medical queries

## 🧪 Testing

### Manual Testing
1. Start the application
2. Open the web interface
3. Try sample questions:
   - "What is the recommended dosage for Humira?"
   - "What are the contraindications for adalimumab?"
   - "How should I store this medication?"

### Health Check
```bash
curl http://localhost:12000/health
```

Expected response:
```json
{
  "status": "healthy",
  "chatbot_initialized": true,
  "chatbot_responsive": true,
  "timestamp": "2025-08-27T10:00:00.000000"
}
```

## 🚨 Medical Disclaimer

**IMPORTANT**: This chatbot is designed for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 🛠️ Development

### Adding New Features
1. **Backend**: Modify `flask_app.py` for new routes
2. **Frontend**: Update templates and static files
3. **Chatbot Logic**: Extend `chatbot.py` for new functionality
4. **PDF Processing**: Enhance `pdf_processor.py` for document handling

### Customization
- **Styling**: Modify `static/css/style.css`
- **JavaScript**: Update `static/js/app.js`
- **Templates**: Customize HTML templates in `templates/`
- **Configuration**: Adjust settings in `config.py`

## 📝 Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not found"**:
   - Ensure you have set the GOOGLE_API_KEY environment variable
   - Check your .env file

2. **"Port already in use"**:
   - Change the PORT environment variable
   - Kill existing processes using the port

3. **"Failed to process PDF"**:
   - Ensure the PDF is not corrupted
   - Check file size (max 16MB)
   - Verify PDF contains readable text

4. **"Chatbot not responding"**:
   - Check your internet connection
   - Verify Google API key is valid
   - Check the health endpoint

### Logs
- Application logs are written to `flask_app.log`
- Check browser console for frontend errors
- Use the health endpoint to verify system status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Sentence Transformers for embeddings
- FAISS for vector similarity search
- Flask for the web framework
- Bootstrap for UI components