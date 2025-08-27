import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from config import Config

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2 embeddings
        self.index = None
        self.documents = []
        self.vector_db_path = Config.VECTOR_DB_PATH
        
        # Create vector database directory if it doesn't exist
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        # Try to load existing index
        self.load_index()
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of texts
        """
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return np.array(embeddings).astype('float32')
    
    def build_index(self, documents: List[Dict[str, any]]):
        """
        Build FAISS index from documents
        """
        if not documents:
            print("No documents provided to build index")
            return
        
        print(f"Building vector index for {len(documents)} documents...")
        
        # Extract texts for embedding
        texts = [doc['text'] for doc in documents]
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        # Store documents
        self.documents = documents
        
        print(f"Vector index built with {self.index.ntotal} vectors")
        
        # Save index
        self.save_index()
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, any], float]]:
        """
        Search for similar documents
        Returns list of (document, similarity_score) tuples
        """
        if self.index is None or len(self.documents) == 0:
            print("No index available. Please build index first.")
            return []
        
        # Create query embedding
        query_embedding = self.create_embeddings([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, min(k, len(self.documents)))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid index
                results.append((self.documents[idx], float(score)))
        
        return results
    
    def save_index(self):
        """
        Save FAISS index and documents to disk
        """
        try:
            if self.index is not None:
                # Save FAISS index
                index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
                faiss.write_index(self.index, index_path)
                
                # Save documents
                docs_path = os.path.join(self.vector_db_path, "documents.pkl")
                with open(docs_path, 'wb') as f:
                    pickle.dump(self.documents, f)
                
                print(f"Index saved to {self.vector_db_path}")
        
        except Exception as e:
            print(f"Error saving index: {str(e)}")
    
    def load_index(self):
        """
        Load FAISS index and documents from disk
        """
        try:
            index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
            docs_path = os.path.join(self.vector_db_path, "documents.pkl")
            
            if os.path.exists(index_path) and os.path.exists(docs_path):
                # Load FAISS index
                self.index = faiss.read_index(index_path)
                
                # Load documents
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                
                print(f"Loaded index with {len(self.documents)} documents")
                return True
        
        except Exception as e:
            print(f"Error loading index: {str(e)}")
        
        return False
    
    def get_relevant_context(self, query: str, max_chunks: int = 5) -> Tuple[str, List[str]]:
        """
        Get relevant context for a query and return citations
        """
        results = self.search(query, k=max_chunks)
        
        if not results:
            return "", []
        
        context_parts = []
        citations = []
        
        for doc, score in results:
            context_parts.append(doc['text'])
            citation = f"{doc['source']} (Page {doc['page']})"
            if citation not in citations:
                citations.append(citation)
        
        context = "\n\n".join(context_parts)
        return context, citations
    
    def update_index(self, new_documents: List[Dict[str, any]]):
        """
        Update index with new documents
        """
        if not new_documents:
            return
        
        # Combine with existing documents
        all_documents = self.documents + new_documents
        
        # Rebuild index
        self.build_index(all_documents)