from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView
from django.contrib.auth.views import LoginView
import requests
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import authenticate,login,logout
from .forms import *
# Create your views here.


def custom_logout(request):
    auth_logout(request)
    return redirect('log')


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = LogForm

    def form_valid(self, form):
        user = form.cleaned_data['user']
        print(user)
        login(self.request, user)  # Logs the user in
        if user.is_superuser:
            return redirect('ah')  # Redirect for superusers
        else:
            return redirect('uh')  # Redirect for normal users

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



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


class ChatbotView(TemplateView):
    template_name='chatbot.html'

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