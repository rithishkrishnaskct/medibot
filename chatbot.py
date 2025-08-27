import os
from typing import Dict, List, Tuple, Optional
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from gemini_client import GeminiClient
from session_manager import SessionManager
from config import Config

class MedicalChatbot:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()
        self.gemini_client = GeminiClient()
        self.session_manager = SessionManager()
        self.is_initialized = False
    
    def initialize(self, pdf_directory: str = None):
        """
        Initialize the chatbot by processing PDFs and building vector index
        """
        if pdf_directory is None:
            pdf_directory = Config.PDF_STORAGE_PATH
        
        print("Initializing Medical Chatbot...")
        
        # Process PDFs
        documents = self.pdf_processor.process_all_pdfs(pdf_directory)
        
        if not documents:
            print("Warning: No documents found. The chatbot will have limited functionality.")
            self.is_initialized = True
            return
        
        # Build or update vector index
        self.vector_store.build_index(documents)
        
        self.is_initialized = True
        print("Medical Chatbot initialized successfully!")
    
    def add_pdf(self, pdf_path: str):
        """
        Add a new PDF to the knowledge base
        """
        if not os.path.exists(pdf_path):
            return False, f"PDF file not found: {pdf_path}"
        
        try:
            # Process the new PDF
            documents = self.pdf_processor.extract_text_from_pdf(pdf_path)
            
            if not documents:
                return False, "Failed to extract text from PDF"
            
            # Update vector index
            self.vector_store.update_index(documents)
            
            return True, f"Successfully added {len(documents)} chunks from {os.path.basename(pdf_path)}"
        
        except Exception as e:
            return False, f"Error adding PDF: {str(e)}"
    
    def create_session(self) -> str:
        """
        Create a new chat session
        """
        return self.session_manager.create_session()
    
    def chat(self, session_id: str, user_message: str) -> Dict[str, any]:
        """
        Process a user message and return response with metadata
        """
        if not self.is_initialized:
            return {
                'response': "Chatbot is not initialized. Please initialize with PDF documents first.",
                'citations': [],
                'session_id': session_id,
                'error': True
            }
        
        if not self.session_manager.session_exists(session_id):
            session_id = self.session_manager.create_session()
        
        try:
            # Get relevant context from vector store
            context, citations = self.vector_store.get_relevant_context(user_message)
            
            # Get conversation history for context awareness
            conversation_history = self.session_manager.get_conversation_history(session_id, limit=3)
            
            # Generate response using Gemini
            response = self.gemini_client.generate_response(
                query=user_message,
                context=context,
                citations=citations,
                conversation_history=conversation_history
            )
            
            # Add to session history
            self.session_manager.add_conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_response=response,
                context_used=citations
            )
            
            return {
                'response': response,
                'citations': citations,
                'session_id': session_id,
                'context_found': bool(context),
                'error': False
            }
        
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            
            # Still add to session history for continuity
            self.session_manager.add_conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_response=error_response,
                context_used=[]
            )
            
            return {
                'response': error_response,
                'citations': [],
                'session_id': session_id,
                'error': True
            }
    
    def get_session_history(self, session_id: str) -> List[Dict[str, any]]:
        """
        Get conversation history for a session
        """
        return self.session_manager.get_conversation_history(session_id)
    
    def clear_session(self, session_id: str):
        """
        Clear conversation history for a session
        """
        self.session_manager.clear_session(session_id)
    
    def get_available_documents(self) -> List[Dict[str, any]]:
        """
        Get list of available documents in the knowledge base
        """
        if not self.vector_store.documents:
            return []
        
        # Group documents by source
        doc_info = {}
        for doc in self.vector_store.documents:
            source = doc['source']
            if source not in doc_info:
                doc_info[source] = {
                    'filename': source,
                    'chunks': 0,
                    'pages': set()
                }
            
            doc_info[source]['chunks'] += 1
            doc_info[source]['pages'].add(doc['page'])
        
        # Convert to list format
        result = []
        for source, info in doc_info.items():
            result.append({
                'filename': info['filename'],
                'total_chunks': info['chunks'],
                'total_pages': len(info['pages']),
                'page_range': f"{min(info['pages'])}-{max(info['pages'])}"
            })
        
        return result
    
    def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, any]]:
        """
        Search documents for specific content
        """
        if not self.is_initialized:
            return []
        
        results = self.vector_store.search(query, k=limit)
        
        return [
            {
                'text': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text'],
                'source': doc['source'],
                'page': doc['page'],
                'similarity_score': float(score),
                'chunk_id': doc['chunk_id']
            }
            for doc, score in results
        ]
    
    def get_system_status(self) -> Dict[str, any]:
        """
        Get system status and statistics
        """
        return {
            'initialized': self.is_initialized,
            'total_documents': len(self.vector_store.documents) if self.vector_store.documents else 0,
            'active_sessions': len(self.session_manager.get_all_sessions()),
            'vector_index_size': self.vector_store.index.ntotal if self.vector_store.index else 0,
            'available_documents': len(self.get_available_documents())
        }