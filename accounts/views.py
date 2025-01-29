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


class ChatbotView(TemplateView):
    template_name='chatbot.html'

class HomeView(TemplateView):
    template_name='home.html'

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