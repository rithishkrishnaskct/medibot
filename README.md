# Medical Drug Information Chatbot

A GenAI-enabled chatbot that extracts prescribing and patient information from drug documentation PDFs and provides contextually aware responses using Google's Gemini API.

## Features

✅ **PDF Document Processing**: Extract text from medical PDFs with page reference tracking  
✅ **RAG (Retrieval Augmented Generation)**: Vector-based document search using FAISS  
✅ **Contextual Awareness**: Maintains conversation history within sessions  
✅ **Citation Support**: Provides source references for all responses  
✅ **Medical Context Filtering**: Only responds to medical/drug-related queries  
✅ **Web Interface**: User-friendly Streamlit interface  
✅ **Session Management**: Multiple concurrent user sessions  

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd medibot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Gemini API key
   ```

4. **Add medical PDFs**:
   - Place your drug information PDFs in the `pdfs/` directory
   - Or upload them through the web interface

## Usage

### Running the Web Interface

```bash
streamlit run app.py --server.host 0.0.0.0 --server.port 12000
```

The application will be available at `http://localhost:12000`

### API Key Setup

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter the API key in the sidebar of the web interface
3. Click "Initialize Chatbot"

### Using the Chatbot

1. **Ask medical questions** about medications, dosages, interactions, etc.
2. **Upload PDFs** containing drug information through the sidebar
3. **Search documents** using the search functionality
4. **View citations** for all responses

### Example Questions

- "What is the recommended dosage for Humira?"
- "What are the contraindications for Skyrizi?"
- "Are there any drug interactions I should be aware of?"
- "What are the common side effects of this medication?"

## Architecture

### Components

1. **PDFProcessor** (`pdf_processor.py`): Extracts text from PDFs with page tracking
2. **VectorStore** (`vector_store.py`): FAISS-based vector database for document embeddings
3. **GeminiClient** (`gemini_client.py`): Google Gemini API integration with medical filtering
4. **SessionManager** (`session_manager.py`): Conversation history and context management
5. **MedicalChatbot** (`chatbot.py`): Main orchestrator class
6. **Streamlit App** (`app.py`): Web interface

### Data Flow

```
PDF Documents → Text Extraction → Vector Embeddings → FAISS Index
                                                           ↓
User Query → Context Retrieval → Gemini API → Response with Citations
```

## Configuration

Edit `config.py` to customize:

- **Chunk size and overlap** for document processing
- **Maximum tokens and temperature** for Gemini API
- **Medical keywords** for context validation
- **Session and conversation limits**

## Medical Disclaimer

⚠️ **Important**: This chatbot provides information for educational purposes only. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment decisions.

## Security Notes

- API keys are handled securely and not stored permanently
- Session data is kept in memory only
- No personal health information is stored

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not found"**
   - Ensure you've entered your API key in the sidebar
   - Check that the API key is valid and has Gemini API access

2. **"No documents found"**
   - Add PDF files to the `pdfs/` directory
   - Or upload PDFs through the web interface

3. **Slow responses**
   - Large PDFs may take time to process initially
   - Subsequent queries should be faster due to caching

### Performance Optimization

- Keep PDF files under 50MB for optimal performance
- Use specific medical terminology in queries for better results
- Clear conversation history periodically to free memory

## Development

### Project Structure

```
medibot/
├── app.py                 # Streamlit web interface
├── chatbot.py            # Main chatbot orchestrator
├── config.py             # Configuration settings
├── gemini_client.py      # Google Gemini API client
├── pdf_processor.py      # PDF text extraction
├── session_manager.py    # Session and conversation management
├── vector_store.py       # Vector database operations
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── pdfs/                # PDF storage directory
├── vector_db/           # Vector database storage
└── README.md            # This file
```

### Adding New Features

1. **Custom PDF Processors**: Extend `PDFProcessor` for specialized document types
2. **Additional LLM Support**: Create new client classes following `GeminiClient` pattern
3. **Enhanced UI**: Modify `app.py` to add new interface elements
4. **Analytics**: Extend `SessionManager` for usage tracking

## License

This project is provided as-is for educational and research purposes.