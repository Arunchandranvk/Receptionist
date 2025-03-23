# chatbot.py
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("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")

# Fallback to using Claude API if GROQ is not available
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# PDF directory path - adjust this based on your Django project structure
PDF_PATH = "College_FAQ"

class PDFChatbot:
    def __init__(self):
        self.vectorstore = None
        self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        self.process_pdfs()
        
    def process_pdfs(self):
        """Process all PDFs in the specified directory"""
        logger.info(f"Processing PDFs from {PDF_PATH}")
        
        if not os.path.exists(PDF_PATH):
            logger.warning(f"PDF directory {PDF_PATH} does not exist")
            os.makedirs(PDF_PATH, exist_ok=True)
            return
            
        pdf_text = ""
        pdf_count = 0
        
        # Get all PDF files from the directory
        for file in os.listdir(PDF_PATH):
            if file.endswith('.pdf'):
                file_path = os.path.join(PDF_PATH, file)
                logger.info(f"Processing PDF: {file_path}")
                extracted_text = self.extract_text_from_pdf(file_path)
                pdf_text += extracted_text
                pdf_count += 1
                
        logger.info(f"Processed {pdf_count} PDF files")
        
        # Process text if PDFs were found
        if pdf_text:
            text_chunks = self.get_text_chunks(pdf_text)
            logger.info(f"Created {len(text_chunks)} text chunks")
            self.vectorstore = self.get_vectorstore(text_chunks)
            logger.info("Vector store created successfully")
        else:
            logger.warning("No PDF text was extracted")
            
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a single PDF file"""
        text = ""
        try:
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
        return text
        
    def get_text_chunks(self, text):
        """Split text into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
        
    def get_vectorstore(self, text_chunks):
        """Create vector store from text chunks"""
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
            return vectorstore
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            return None
            
    def get_conversation_chain(self):
        """Create conversation chain with LLM"""
        if not self.vectorstore:
            logger.warning("No vector store available")
            return None
            
        try:
            # Try to use Groq first
            if GROQ_API_KEY:
                logger.info("Using Groq LLM")
                llm = ChatGroq(
                    api_key=GROQ_API_KEY,
                    model_name="llama2-70b-4096",
                    temperature=0.1
                )
            # Fallback to Claude if Groq is not available
            elif CLAUDE_API_KEY:
                logger.info("Using Claude LLM")
                from langchain.llms import Anthropic
                llm = Anthropic(
                    api_key=CLAUDE_API_KEY,
                    model="claude-2",
                    temperature=0.1
                )
            else:
                logger.error("No API keys available for LLMs")
                return None
                
            conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(),
                memory=self.memory
            )
            return conversation_chain
        except Exception as e:
            logger.error(f"Error creating conversation chain: {e}")
            return None
            
    def ask_question(self, question):
        """Ask a question and get response"""
        logger.info(f"Question received: {question}")
        
        if not self.vectorstore:
            return "I don't have any college information loaded yet. Please contact the administrator to load the college documents."
            
        conversation_chain = self.get_conversation_chain()
        if not conversation_chain:
            return "I'm having trouble accessing my knowledge. Please try again later."
            
        try:
            response = conversation_chain({"question": question})
            logger.info("Response generated successfully")
            return response["answer"]
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I couldn't process your question at this time. Please try again later."