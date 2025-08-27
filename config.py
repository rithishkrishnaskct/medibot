import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    
    # Medical context keywords for validation
    MEDICAL_KEYWORDS = [
        "drug", "medication", "medicine", "prescription", "dosage", "dose",
        "contraindication", "side effect", "adverse", "interaction", "treatment",
        "therapy", "pharmaceutical", "clinical", "patient", "healthcare",
        "medical", "diagnosis", "symptom", "disease", "condition", "health",
        "administration", "indication", "precaution", "warning", "safety"
    ]
    
    # Vector database settings
    VECTOR_DB_PATH = "./vector_db"
    PDF_STORAGE_PATH = "./pdfs"
    
    # Session settings
    MAX_CONVERSATION_HISTORY = 10