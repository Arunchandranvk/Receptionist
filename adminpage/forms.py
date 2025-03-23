from  django import forms  
from accounts.models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['std_id']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['std_id','password']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'name', 'email', 'phone', 'department', 
                 'designation', 'profile_picture', 'join_date']
        widgets = {
            'teacher_id': forms.TextInput(attrs={'class': 'w-full border rounded p-2', 'placeholder': 'Enter teacher ID'}),
            'name': forms.TextInput(attrs={'class': 'w-full border rounded p-2', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded p-2', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border rounded p-2', 'placeholder': 'Enter phone number'}),
            'designation': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'join_date': forms.DateInput(attrs={'class': 'w-full border rounded p-2', 'type': 'date'}),
        }