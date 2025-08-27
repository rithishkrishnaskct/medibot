"""
Test script for the Medical Chatbot
"""
import os
import sys
from chatbot import MedicalChatbot
from config import Config

def test_chatbot():
    """Test the medical chatbot functionality"""
    
    print("🧪 Testing Medical Chatbot")
    print("=" * 50)
    
    # Check if API key is set
    if not Config.GOOGLE_API_KEY:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your API key in .env file or environment")
        return False
    
    try:
        # Initialize chatbot
        print("🚀 Initializing chatbot...")
        chatbot = MedicalChatbot()
        chatbot.initialize()
        
        # Create session
        session_id = chatbot.create_session()
        print(f"✅ Session created: {session_id}")
        
        # Test queries
        test_queries = [
            "What is the recommended dosage for Humira?",
            "What are the contraindications for adalimumab?",
            "Are there any drug interactions I should be aware of?",
            "What are the common side effects?",
            "How should I store this medication?",
            "What is the weather today?"  # Non-medical query
        ]
        
        print("\n💬 Testing queries:")
        print("-" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            
            response_data = chatbot.chat(session_id, query)
            
            print(f"   Response: {response_data['response'][:200]}...")
            if response_data['citations']:
                print(f"   Citations: {', '.join(response_data['citations'])}")
            else:
                print("   Citations: None")
            print(f"   Context Found: {response_data['context_found']}")
            print(f"   Error: {response_data['error']}")
        
        # Test system status
        print("\n📊 System Status:")
        print("-" * 20)
        status = chatbot.get_system_status()
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test document search
        print("\n🔍 Testing document search:")
        print("-" * 30)
        search_results = chatbot.search_documents("dosage", limit=3)
        for i, result in enumerate(search_results, 1):
            print(f"   {i}. {result['source']} (Page {result['page']}) - Score: {result['similarity_score']:.3f}")
            print(f"      {result['text'][:100]}...")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def create_sample_pdfs():
    """Create sample PDFs for testing"""
    try:
        print("📄 Creating sample PDFs...")
        exec(open('create_sample_pdf.py').read())
        return True
    except Exception as e:
        print(f"⚠️  Could not create sample PDFs: {str(e)}")
        print("You can manually add PDF files to the pdfs/ directory")
        return False

if __name__ == "__main__":
    print("🏥 Medical Chatbot Test Suite")
    print("=" * 50)
    
    # Create sample PDFs first
    create_sample_pdfs()
    
    # Run tests
    success = test_chatbot()
    
    if success:
        print("\n🎉 All tests passed! The chatbot is ready to use.")
        print("\nTo start the web interface, run:")
        print("streamlit run app.py --server.host 0.0.0.0 --server.port 12000")
    else:
        print("\n❌ Tests failed. Please check the configuration and try again.")
    
    sys.exit(0 if success else 1)