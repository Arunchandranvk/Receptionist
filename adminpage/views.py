from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,View,UpdateView
from accounts.models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class AdminHomeView(TemplateView):
    template_name='admin_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stu']= Student.objects.first()
        context['event']=Event.objects.first()
        context['noti']=Notification.objects.first()
        return context

class FacultyView(TemplateView):
    template_name='faculty_view.html'



class StudentView(View):
    template_name = 'student_view.html'
    
    def get(self, request, *args, **kwargs):
        student = Student.objects.all()
        count = student.count()
        department = Department.objects.all()
        context = {
            'students':student,
            'department':department,
            'count':count
            
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('student')
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            students = Student.objects.all()
            context = {
                'students': students,
                'form': form
            }
            return render(request, self.template_name, context)


class StudentPUTView(View): 
    template_name = 'student_edit.html'
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        student = get_object_or_404(Student, id=id)
        department = Department.objects.all()
        form = StudentForm(instance=student)
        
        context = {
            'form': form,
            'student': student,
            'department': department
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        stu = get_object_or_404(Student, id=id)
        form = StudentForm(request.POST, request.FILES, instance=stu)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Student Updated Successfully!")
            return redirect('student')  # Ensure correct URL name
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            department = Department.objects.all()
            context = {
                'form': form,
                'student': stu,
                'department': department
            }
            return render(request, self.template_name, context)
        
def StudentDeleteView(req,pk):
    stu = Student.objects.get(id=pk)
    stu.delete()
    return redirect('student')

class DepartmentView(TemplateView):
    template_name = 'department.html'
    
    def get(self, request, *args, **kwargs):
        department = Department.objects.all()
        context = {
            'department':department
            
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('dep')
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            context = {
                'form': form
            }
            return render(request, self.template_name, context)

def DepartmentDeleteView(req,pk):
    dep = Department.objects.get(id=pk)
    dep.delete()
    return redirect('dep')
    

class EventView(View):
    template_name = 'event_view.html'
    
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        count = event.count()
        context = {
            'events':event,
            'count':count
            
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Added Successfully!")
            return redirect('event')
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            event = Event.objects.all()
            context = {
                'events': event,
                'form': form
            }
            return render(request, self.template_name, context)


class EventPUTView(View): 
    template_name = 'event_edit.html'
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        event = get_object_or_404(Event, id=id)
        form = EventForm(instance=event)
        context = {
            'form': form,
            'event': event,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        event = get_object_or_404(Event, id=id)
        form = EventForm(request.POST, request.FILES, instance=event)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully!")
            return redirect('event') 
        
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            context = {
                'form': form,
                'event': event,
            }
            return render(request, self.template_name, context)
        
def EventDeleteView(req,pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('event')

class NotificationView(View):
    template_name = 'notification.html'
    
    def get(self, request, *args, **kwargs):
        notification = Notification.objects.all().order_by('-created_at')
        count = notification.count()
        context = {
            'noti':notification,
            'count':count
            
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Notification Added Successfully!")
            return redirect('notification')
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            notification = Notification.objects.all()
            context = {
                'noti': notification,
                'form': form
            }
            return render(request, self.template_name, context)


class NotificationPUTView(View): 
    template_name = 'notification_edit.html'
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        noti = get_object_or_404(Notification, id=id)
        form = NotificationForm(instance=noti)
        context = {
            'form': form,
            'noti': noti,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        notification = get_object_or_404(Notification, id=id)
        form = NotificationForm(request.POST, request.FILES, instance=notification)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Notification Updated Successfully!")
            return redirect('notification') 
        
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            context = {
                'form': form,
                'noti': notification,
            }
            return render(request, self.template_name, context)
        
def NotificationDeleteView(req,pk):
    noti = Notification.objects.get(id=pk)
    noti.delete()
    return redirect('notification')