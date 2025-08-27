import streamlit as st
import os
import time
from chatbot import MedicalChatbot
from config import Config

# Page configuration
st.set_page_config(
    page_title="Medical Drug Information Chatbot",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .citation {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .status-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.initialized = False

def initialize_chatbot():
    """Initialize the chatbot"""
    try:
        with st.spinner("Initializing Medical Chatbot... This may take a few moments."):
            chatbot = MedicalChatbot()
            chatbot.initialize()
            st.session_state.chatbot = chatbot
            st.session_state.session_id = chatbot.create_session()
            st.session_state.initialized = True
            st.success("✅ Medical Chatbot initialized successfully!")
            return True
    except Exception as e:
        st.error(f"❌ Failed to initialize chatbot: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">💊 Medical Drug Information Chatbot</h1>', unsafe_allow_html=True)
    
    # Medical disclaimer
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Medical Disclaimer:</strong> This chatbot provides information for educational purposes only. 
        Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment decisions.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Controls")
        
        # API Key input
        api_key = st.text_input("Google API Key", type="password", 
                               value=os.getenv("GOOGLE_API_KEY", ""),
                               help="Enter your Google Gemini API key")
        
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            Config.GOOGLE_API_KEY = api_key
        
        # Initialize button
        if st.button("🚀 Initialize Chatbot", disabled=st.session_state.initialized):
            if not api_key:
                st.error("Please enter your Google API key first!")
            else:
                initialize_chatbot()
        
        # System status
        if st.session_state.initialized and st.session_state.chatbot:
            st.subheader("📊 System Status")
            status = st.session_state.chatbot.get_system_status()
            st.metric("Documents Loaded", status['total_documents'])
            st.metric("Active Sessions", status['active_sessions'])
            st.metric("Vector Index Size", status['vector_index_size'])
        
        # Document management
        st.subheader("📚 Document Management")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
        if uploaded_file and st.session_state.initialized:
            if st.button("📄 Add PDF to Knowledge Base"):
                # Save uploaded file
                pdf_path = os.path.join(Config.PDF_STORAGE_PATH, uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Add to chatbot
                success, message = st.session_state.chatbot.add_pdf(pdf_path)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        # Available documents
        if st.session_state.initialized and st.session_state.chatbot:
            docs = st.session_state.chatbot.get_available_documents()
            if docs:
                st.subheader("📋 Available Documents")
                for doc in docs:
                    st.text(f"📄 {doc['filename']}")
                    st.text(f"   Pages: {doc['page_range']}")
                    st.text(f"   Chunks: {doc['total_chunks']}")
        
        # Session controls
        if st.session_state.initialized:
            st.subheader("💬 Session Controls")
            if st.button("🗑️ Clear Conversation"):
                if st.session_state.chatbot and st.session_state.session_id:
                    st.session_state.chatbot.clear_session(st.session_state.session_id)
                    st.session_state.messages = []
                    st.success("Conversation cleared!")
    
    # Main chat interface
    if not st.session_state.initialized:
        st.info("👆 Please enter your Google API key and click 'Initialize Chatbot' to get started.")
        
        # Instructions
        st.subheader("📖 How to Use")
        st.markdown("""
        1. **Enter your Google Gemini API Key** in the sidebar
        2. **Click 'Initialize Chatbot'** to load the system
        3. **Upload PDF documents** containing drug information (optional)
        4. **Start asking medical questions** about medications, dosages, interactions, etc.
        
        **Example Questions:**
        - "What is the recommended dosage for Humira?"
        - "What are the contraindications for Skyrizi?"
        - "Are there any drug interactions I should be aware of?"
        - "What are the common side effects of this medication?"
        """)
        
        return
    
    # Chat interface
    st.subheader("💬 Chat with Medical Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            citations_html = ""
            if message.get("citations"):
                citations_html = f"""
                <div class="citation">
                    📚 Sources: {", ".join(message["citations"])}
                </div>
                """
            
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Medical Assistant:</strong><br>
                {message["content"]}
                {citations_html}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask a medical question...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response from chatbot
        with st.spinner("🔍 Searching medical documents and generating response..."):
            response_data = st.session_state.chatbot.chat(st.session_state.session_id, user_input)
        
        # Add assistant response to chat
        assistant_message = {
            "role": "assistant", 
            "content": response_data["response"],
            "citations": response_data.get("citations", [])
        }
        st.session_state.messages.append(assistant_message)
        
        # Rerun to display new messages
        st.rerun()
    
    # Search functionality
    with st.expander("🔍 Search Documents"):
        search_query = st.text_input("Search for specific content in documents:")
        if search_query and st.session_state.chatbot:
            results = st.session_state.chatbot.search_documents(search_query, limit=5)
            
            if results:
                st.subheader("Search Results:")
                for i, result in enumerate(results, 1):
                    st.markdown(f"""
                    **Result {i}** (Score: {result['similarity_score']:.3f})
                    
                    📄 **Source:** {result['source']} (Page {result['page']})
                    
                    **Content:** {result['text']}
                    
                    ---
                    """)
            else:
                st.info("No results found for your search query.")

if __name__ == "__main__":
    main()