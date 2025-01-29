from django.urls import path
from .views import *

urlpatterns = [
    path('user-home/',UserhomeView.as_view(),name='uh'),
    path('user-course/',UserCourseView.as_view(),name='u-course'),
    path('user-profile/',ProfileView.as_view(),name='u-profile'),
    path('user-profile-edit/<int:pk>/',ProfilePUTView.as_view(),name='u-profileedit'),
    path('user-events/',EventView.as_view(),name='u-event'),
    path('user-notification/',NotificationView.as_view(),name='u-notification'),
]
