from django.urls import path
from .views import *

urlpatterns = [
    path('',MainHomeView.as_view(),name='mh'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('chatbot/',ChatbotView.as_view(),name='bot'),
    path('home/',HomeView.as_view(),name='h'),
    path('course/',CourseView.as_view(),name='course'),
    path('chatbot/send_message/', send_message_to_rasa, name='send_message_to_rasa'),   
]