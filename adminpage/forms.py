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
