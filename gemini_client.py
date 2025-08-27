import google.generativeai as genai
from typing import List, Dict, Optional
from config import Config

class GeminiClient:
    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompt for medical context
        self.system_prompt = """
You are a specialized medical information assistant focused on drug and medication information. 
Your role is to provide accurate, evidence-based information about medications, including:

- Prescribing information (dosage, administration, contraindications)
- Drug interactions and precautions
- Side effects and adverse reactions
- Patient-specific advice and safety information
- Therapeutic indications and usage guidelines

IMPORTANT GUIDELINES:
1. Only respond to medical and drug-related queries
2. Always provide citations from the source documents when available
3. If a question is not medical/drug-related, politely redirect the user
4. Never provide personal medical advice - always recommend consulting healthcare professionals
5. Be precise and factual, avoiding speculation
6. If information is not available in the provided context, clearly state this limitation

Format your responses with:
- Clear, structured information
- Proper citations in the format [Source: filename (Page X)]
- Appropriate medical disclaimers when necessary
"""
    
    def is_medical_query(self, query: str) -> bool:
        """
        Check if the query is related to medical/drug information
        """
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in Config.MEDICAL_KEYWORDS)
    
    def generate_response(self, query: str, context: str, citations: List[str], 
                         conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate response using Gemini API with context and citations
        """
        if not self.is_medical_query(query):
            return """I'm a specialized medical information assistant focused on drug and medication information. 
I can only help with medical and drug-related queries such as:
- Medication dosages and administration
- Drug interactions and contraindications
- Side effects and precautions
- Prescribing information
- Patient safety information

Please ask a medical or drug-related question, and I'll be happy to help!"""
        
        # Build conversation context
        conversation_context = ""
        if conversation_history:
            conversation_context = "\n\nPrevious conversation context:\n"
            for entry in conversation_history[-3:]:  # Last 3 exchanges
                conversation_context += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n\n"
        
        # Build citations text
        citations_text = ""
        if citations:
            citations_text = f"\n\nAvailable sources: {', '.join(citations)}"
        
        # Construct the full prompt
        prompt = f"""{self.system_prompt}

Context from medical documents:
{context}
{citations_text}
{conversation_context}

User Question: {query}

Please provide a comprehensive response based on the available context. Include proper citations for any information you reference from the documents."""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=Config.TEMPERATURE,
                    max_output_tokens=Config.MAX_TOKENS,
                )
            )
            
            return response.text
        
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again or rephrase your question."
    
    def generate_summary(self, text: str) -> str:
        """
        Generate a summary of the provided text
        """
        prompt = f"""Please provide a concise summary of the following medical document content, 
focusing on key drug information, dosages, contraindications, and safety information:

{text}

Summary:"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=500,
                )
            )
            
            return response.text
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def validate_medical_content(self, text: str) -> bool:
        """
        Validate if the content is medical/drug-related
        """
        prompt = f"""Is the following text related to medical information, drugs, medications, or healthcare? 
Respond with only 'YES' or 'NO':

{text[:500]}"""  # Limit text length for validation
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    max_output_tokens=10,
                )
            )
            
            return response.text.strip().upper() == 'YES'
        
        except Exception as e:
            print(f"Error validating content: {str(e)}")
            return False