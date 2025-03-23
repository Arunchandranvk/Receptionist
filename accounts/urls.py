from django.urls import path
from .views import *

urlpatterns = [
    path('',MainHomeView.as_view(),name='mh'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('chatbot/',ChatbotView.as_view(),name='bot'),
    path('response/',chatbot_api,name='chatbot'),
    path('home/',HomeView.as_view(),name='h'),
    path('course/',CourseView.as_view(),name='course'),
    path('chatbot/send_message/', send_message_to_rasa, name='send_message_to_rasa'),   
    path('enquire/', enquiry_view, name='enquiry'),
    path('enquire/success/', enquiry_success_view, name='enquiry_success'),
    path('send-verification/', SendVerificationView.as_view(), name='send_verification'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
]

