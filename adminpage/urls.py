from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin-home/',AdminHomeView.as_view(),name='ah'),
    path('faculty/', FacultyView.as_view(), name='faculty'),
    path('faculty/add/', AddTeacherView.as_view(), name='add_teacher'),
    path('faculty/delete/<int:pk>/', DeleteTeacherView.as_view(), name='delete_teacher'),
    path('student/',StudentView.as_view(),name='student'),
    path('student/<int:pk>/',StudentPUTView.as_view(),name='student-update'),
    path('student-delete/<int:pk>/',StudentDeleteView,name='student-delete'),
    path('faculty-delete/<int:pk>/',FacultyDeleteView,name='faculty-delete'),
    path('event/',EventView.as_view(),name='event'),
    path('event/<int:pk>/',EventPUTView.as_view(),name='event-update'),
    path('event-delete/<int:pk>/',EventDeleteView,name='event-delete'),
    path('notification/',NotificationView.as_view(),name='notification'),
    path('notification/<int:pk>/',NotificationPUTView.as_view(),name='notification-update'),
    path('notification-delete/<int:pk>/',NotificationDeleteView,name='notification-delete'),
    path('department/',DepartmentView.as_view(),name='dep'),
    path('department-delete/<int:pk>/',DepartmentDeleteView,name='dep-delete'),
    path('home/', auth_views.LogoutView.as_view(), name='logout'),
]