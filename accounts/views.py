from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,View
from django.contrib.auth.views import LoginView
import requests
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import login
from .forms import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
# Create your views here.


def custom_logout(request):
    auth_logout(request)
    return redirect('log')


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = LogForm

    def form_valid(self, form):
        user = form.cleaned_data['user'] 
        if not user.is_verified:
            self.request.session['pending_verification_email'] = user.email
            return redirect('send_verification')  
        login(self.request, user)
        if user.is_superuser:
            return redirect('ah')  
        else:
            return redirect('uh') 
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def send_verification_email(user, request):
    """Send verification email to user"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = 'Verify your SNGCE account'
    message = render_to_string('verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
    )


class SendVerificationView(View):
    """View to send verification email"""
    def get(self, request):
        # Get email from session
        email = request.session.get('pending_verification_email')
        
        if not email:
            return redirect('login')
            
        try:
            user = CustomUser.objects.get(email=email)
            send_verification_email(user, request)
            return render(request, 'verification_sent.html', {'email': email})
        except CustomUser.DoesNotExist:
            return redirect('login')


class VerifyEmailView(View):
    """View to verify email via token link"""
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                login(request, user)
                if user.is_superuser:
                    return redirect('ah')
                else:
                    return redirect('uh')
            else:
                return render(request, 'verification_failed.html')
                
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return render(request, 'verification_failed.html')

class MainHomeView(TemplateView):
    template_name='mainhome.html'

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import re

def get_bot_response(user_message):
    # Lowercase the user message to make it case-insensitive
    user_message = user_message.strip().lower()

    faq = {
    "hi": "hello! how can i assist you today?",
    "hello": "hi there! how can i help you?",
    "hey": "hey! what can i do for you?",
    "bye": "goodbye! have a great day!",
    "goodbye": "see you later! take care.",
    "how are you?": "i'm just a bot, but i'm here to help you!",
    "thank you": "you're welcome! let me know if you need anything else.",
    "thanks": "no problem! happy to help.",
    "what is the full name of the college?": "the full name of our college is sree narayana gurukulam college of engineering.",
    "where is the college located?": "the college is located in kerala, india.",
    "what are the office hours of the college?": "the college office is open from 9:00 am to 5:00 pm, monday to saturday.",
    "how can i contact the college?": "you can contact us via phone at [insert phone number] or email at [insert email address].",
    "what is the official website of the college?": "the official website is [insert website link].",
    "how can i apply for admission?": "you can apply online through our website or visit the admission office for offline applications.",
    "what are the eligibility criteria for b.tech admission?": "you need to have passed 12th grade with physics, chemistry, and mathematics, and qualify for entrance exams like keam/jee.",
    "is there any entrance exam for admission?": "yes, keam and jee are accepted for b.tech admissions. other courses may have different requirements.",
    "what documents are required for admission?": "you need to submit 10th & 12th mark sheets, entrance exam scores, transfer certificate, id proof, and passport-size photos.",
    "what is the last date to apply for admission?": "the last date varies every year. please check the official website for the latest updates.",
    "what courses does the college offer?": "the college offers b.tech, m.tech, mba, and other programs in various disciplines.",
    "which engineering branches are available?": "we have computer science, mechanical, civil, electrical, and electronics & communication engineering.",
    "is there a management quota for admission?": "yes, a certain percentage of seats are reserved under the management quota.",
    "does the college offer ph.d. programs?": "no, currently we offer undergraduate and postgraduate courses only.",
    "are there any diploma courses available?": "no, the college currently focuses on degree programs.",
    "what is the tuition fee for b.tech courses?": "the fee structure varies by branch. you can check the detailed fee structure on our website.",
    "does the college offer scholarships?": "yes, we offer merit-based and need-based scholarships.",
    "how can i apply for a scholarship?": "you need to fill out the scholarship application form and provide necessary documents such as academic records and income certificates.",
    "are there any fee concessions for economically weaker students?": "yes, we offer fee concessions based on government norms and college policies.",
    "can i pay the fees in installments?": "yes, installment options are available. please contact the accounts department for details.",
    "does the college have a hostel facility?": "yes, we have separate hostels for boys and girls with all necessary amenities.",
    "what are the hostel fees?": "the hostel fees depend on room type and facilities. you can check the details on our website.",
    "is there a library on campus?": "yes, our library has a vast collection of books, journals, and digital resources.",
    "does the college have wi-fi?": "yes, the entire campus is wi-fi enabled.",
    "are there sports facilities in the college?": "yes, we have facilities for cricket, football, basketball, badminton, and indoor games.",
    "does the college provide placement assistance?": "yes, our placement cell assists students in securing jobs and internships.",
    "which companies visit the college for placements?": "companies like infosys, tcs, wipro, and other mncs participate in our placement drives.",
    "what is the highest package offered in placements?": "the highest package varies yearly but is usually around [mention latest package details].",
    "is there an internship program in the college?": "yes, we have tie-ups with several companies for internships.",
    "what is the duration of the b.tech course?": "the b.tech course duration is 4 years.",
    "what are the hostel facilities available?": "we offer both ac and non-ac rooms with 24/7 water and electricity supply.",
    "are there transport facilities from the college?": "yes, we provide college buses from various locations to the campus.",
    "does the college offer any online courses?": "currently, we offer only offline courses, but we are planning to introduce online courses in the future.",
    "how can i know about the college events and activities?": "you can check our college website, notice boards, or follow us on social media for updates.",
    "what is the admission process for mba?": "the mba admission process includes entrance exams like cat, mat, or kmat and personal interviews.",
    "how can i contact the hostel?": "you can contact the hostel warden or the college administration for hostel inquiries.",
    "what is the curriculum for the computer science engineering branch?": "the curriculum covers programming languages, data structures, algorithms, networking, databases, and more.",
    "is there any fee refund policy?": "yes, the fee refund policy is available as per the guidelines issued by the college and government.",
    "can i get a transcript from the college?": "yes, you can request for a transcript by filling out the application form in the college office.",
    "does the college have an alumni association?": "yes, we have an active alumni association that conducts regular events and meets.",
    "what extra-curricular activities does the college offer?": "the college offers various clubs and activities such as music, dance, drama, debating, and technical clubs.",
    "does the college provide any online courses for students?": "currently, all courses are offline, but we are planning to introduce online courses in the near future.",
    "can i join any club in the college?": "yes, you can join any club based on your interests. visit the student activities office for more details."
}

    # Look for an exact match in the faq dictionary
    response = faq.get(user_message, None)

    # If exact match is not found, try to match using regular expressions for flexible matching
    if not response:
        for key, value in faq.items():
            if re.search(user_message, key):  # Use regex to check for similar meaning
                response = value
                break

    # If no match found, return a default message
    if not response:
        response = "I'm sorry, I don't have an answer to that. Please check our website or contact the college office."

    return response

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if not user_message:
                return JsonResponse({"error": "Empty message received."}, status=400)
            
            bot_response = get_bot_response(user_message)
            return JsonResponse({"response": bot_response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)



class HomeView(TemplateView):
    template_name='home.html'


from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
import os
from .pdf import PDFChatbot
from django.conf import settings
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
import pdfplumber
# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GROQ_API_KEY = "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"

# Fallback to using Claude API if GROQ is not available

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
        """Extract text from a single PDF file using pdfplumber for better accuracy"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
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
        """Create conversation chain with LLM using Groq API"""
        if not self.vectorstore:
            logger.warning("No vector store available")
            return None
            
        try:
            # Try to use Groq first, or fall back to a local model
            if GROQ_API_KEY:
                logger.info("Using Groq LLM")
                llm = ChatGroq(
                    api_key=GROQ_API_KEY,
                    model_name="llama3-8b-8192",
                    temperature=0.1
                )
            # else:
            #     logger.info("Using fallback Claude API or local model")
            #     # Fallback to local model or other API
            #     llm = SomeOtherLLM()
                
            # Create a conversational retriever that queries the vectorstore
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
        """Ask a question and get a more accurate response"""
        logger.info(f"Question received: {question}")
        
        if not self.vectorstore:
            return "I don't have any college information loaded yet. Please contact the administrator to load the documents."
        
        conversation_chain = self.get_conversation_chain()
        if not conversation_chain:
            return "I'm having trouble accessing my knowledge. Please try again later."
        
        try:
            response = conversation_chain({"question": question})
            
            # If the response is too vague, trigger a fallback mechanism
            if "confidence" in response and response["confidence"] < 0.5:
                logger.warning("Low confidence in the response. Triggering fallback.")
                return "I'm not sure about that. Can you please rephrase or try another question?"
            
            logger.info("Response generated successfully")
            return response["answer"]
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I couldn't process your question at this time. Please try again later."

class ChatbotView(TemplateView):
    template_name = 'chatbot.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@csrf_exempt
def chatbot_api(request):
    """API endpoint for chatbot interactions"""
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            language = data.get('language', 'en')
            print(language)
            print(",,,", message)
            if not message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Instantiate the chatbot here
            chatbot = PDFChatbot()  # Create an instance of PDFChatbot
            
            # Check if we should use PDF knowledge or FAQ data
            if message:
                # Use PDF knowledge base
                try:
                    print("000000")
                    response = chatbot.ask_question(message)  # Use the chatbot instance here
                    print("--", response)
                except Exception as e:
                    print(e)
            
            # Translate response if needed
            if language != 'en':
                print("lang",language)
                response = translate_text(response, target_language=language)
                
            return JsonResponse({'response': response})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def get_faq_response(message):
    """Get responses from predefined FAQ data"""
    # Simplified FAQ dictionary - can be expanded or moved to database
    faq = {
        "how are you": "I'm just a bot, but I'm here to help you!",
        "thank you": "You're welcome! Let me know if you need anything else.",
        "thanks": "No problem! Happy to help.",
        "college name": "The full name of our college is Sree Narayana Gurukulam College of Engineering.",
        "location": "The college is located in Kadayiruppu, Kolenchery, Kerala, India.",
        "office hours": "The college office is open from 9:00 AM to 5:00 PM, Monday to Saturday.",
        "contact": "You can contact us via phone at +91-484-2764841 or email at info@sngce.ac.in.",
        "website": "The official website is https://www.sngce.ac.in/",
        "admission": "You can apply online through our website or visit the admission office for offline applications.",
        "eligibility": "For B.Tech admission, you need to have passed 12th grade with Physics, Chemistry, and Mathematics, and qualify for entrance exams like KEAM/JEE.",
        "entrance exam": "Yes, KEAM and JEE are accepted for B.Tech admissions. Other courses may have different requirements.",
        "documents": "You need to submit 10th & 12th mark sheets, entrance exam scores, transfer certificate, ID proof, and passport-size photos.",
        "courses": "The college offers B.Tech, M.Tech, MBA, and other programs in various disciplines.",
        "branches": "We have Computer Science, Mechanical, Civil, Electrical, and Electronics & Communication Engineering.",
        "management quota": "Yes, a certain percentage of seats are reserved under the management quota.",
        "phd": "No, currently we offer undergraduate and postgraduate courses only.",
        "fees": "The fee structure varies by branch. Please check the detailed fee structure on our website.",
        "scholarship": "Yes, we offer merit-based and need-based scholarships.",
        "hostel": "Yes, we have separate hostels for boys and girls with all necessary amenities.",
        "library": "Yes, our library has a vast collection of books, journals, and digital resources.",
        "wifi": "Yes, the entire campus is Wi-Fi enabled.",
        "sports": "Yes, we have facilities for cricket, football, basketball, badminton, and indoor games.",
        "placement": "Yes, our placement cell assists students in securing jobs and internships.",
        "companies": "Companies like Infosys, TCS, Wipro, and other MNCs participate in our placement drives.",
        "transport": "Yes, we provide college buses from various locations to the campus.",
        "events": "You can check our college website, notice boards, or follow us on social media for updates."
    }
    
    # Process input message
    message = message.lower().strip()
    
    # Check for keyword matches
    for key, value in faq.items():
        if key in message:
            return value
    
    # If no match is found
    return "I'm sorry, I didn't have an answer for that specific question. Could you please rephrase or ask something else about SNGCE?"
from deep_translator import GoogleTranslator

# Initialize the translator
translator = GoogleTranslator(target="ml")

def translate_text(text, target_language):
    """
    Translate text to target language.
    Currently, it uses Google Translator API for actual translation.
    """
    if target_language == "ml":
        translated_message = translator.translate(text)  # Automatically detects the source language
    else:
        # If the target language is not Malayalam, handle accordingly
        translated_message = text  # You can add other translations or default behavior as needed.
        
    return translated_message


class CourseView(TemplateView):
    template_name='courses.html'





RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@csrf_exempt  # Exempting CSRF for this view (use cautiously in production)
def send_message_to_rasa(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            user_message = data.get("message")
            if not user_message:
                return JsonResponse({"error": "Message is required"}, status=400)

            # Payload for Rasa
            payload = {
                "sender": "default",  # Or get the sender dynamically
                "message": user_message,
            }

            # Send the message to Rasa
            response = requests.post(RASA_SERVER_URL, json=payload)

            # Check if Rasa server responded successfully
            if response.status_code != 200:
                return JsonResponse({"error": "Failed to communicate with Rasa server"}, status=response.status_code)

            # Parse Rasa response
            response_data = response.json()
            return JsonResponse(response_data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Rasa server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)




# class AddStudent(CreateView):
#     template_name='addstudent.html'
#     model=Student 
#     form_class=StudentForm 
#     success_url=reverse_lazy('students')



# class StudentsList(TemplateView):
#     template_name='students_list.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['students'] = Student.objects.all()
#         return context

from django.contrib import messages

def enquiry_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your enquiry! We'll get back to you soon.")
            return redirect('enquiry_success')
    else:
        form = EnquiryForm()
    
    return render(request, 'enquiry_form.html', {'form': form})

def enquiry_success_view(request):
    return render(request, 'enquiry_success.html')