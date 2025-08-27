import os
import PyPDF2
from typing import List, Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Extract text from PDF and maintain page references for citations
        Returns list of dictionaries with text chunks and metadata
        """
        chunks = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    if page_text.strip():
                        # Split page text into smaller chunks
                        page_chunks = self.text_splitter.split_text(page_text)
                        
                        for chunk_idx, chunk in enumerate(page_chunks):
                            chunks.append({
                                'text': chunk,
                                'source': os.path.basename(pdf_path),
                                'page': page_num + 1,
                                'chunk_id': f"{os.path.basename(pdf_path)}_page_{page_num + 1}_chunk_{chunk_idx + 1}"
                            })
        
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            return []
        
        return chunks
    
    def process_all_pdfs(self, pdf_directory: str) -> List[Dict[str, any]]:
        """
        Process all PDFs in the specified directory
        """
        all_chunks = []
        
        if not os.path.exists(pdf_directory):
            print(f"PDF directory {pdf_directory} does not exist")
            return all_chunks
        
        pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {pdf_directory}")
            return all_chunks
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_file)
            print(f"Processing {pdf_file}...")
            
            chunks = self.extract_text_from_pdf(pdf_path)
            all_chunks.extend(chunks)
            
            print(f"Extracted {len(chunks)} chunks from {pdf_file}")
        
        print(f"Total chunks extracted: {len(all_chunks)}")
        return all_chunks
    
    def get_pdf_metadata(self, pdf_path: str) -> Dict[str, str]:
        """
        Extract metadata from PDF file
        """
        metadata = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': str(pdf_reader.metadata.get('/CreationDate', '')),
                        'modification_date': str(pdf_reader.metadata.get('/ModDate', ''))
                    }
                
                metadata['num_pages'] = len(pdf_reader.pages)
                metadata['filename'] = os.path.basename(pdf_path)
        
        except Exception as e:
            print(f"Error extracting metadata from {pdf_path}: {str(e)}")
        
        return metadata