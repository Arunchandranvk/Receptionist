from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,View,UpdateView
from accounts.models import *
from adminpage.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class UserhomeView(TemplateView):
    template_name = "userhome.html"

class UserCourseView(TemplateView):
    template_name = "course.html"

# class ProfileView(TemplateView):
#     template_name = "profile.html"
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         user = self.request.user
#         print(user.id)
#         stu = CustomUser.objects.get(id=user.id)
#         context['user'] = Student.objects.get(id=stu.id)
#         return context

class ProfileView(View):
    template_name = 'profile.html'
    def get(self, request, *args, **kwargs):
        print(request.user)
        user = CustomUser.objects.get(id=request.user.id)
        student = Student.objects.get(id=user.id)
        context = {
            'user':student
            
        }
        return render(request, self.template_name, context)
    
 


class ProfilePUTView(View): 
    template_name = 'profile_edit.html'
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        student = get_object_or_404(Student, id=id)
        form = StudentForm(instance=student)
        dep = Department.objects.all()
        context = {
            'form': form,
            'user': student,
            'department':dep
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        stu = get_object_or_404(Student, id=id)
        form = ProfileForm(request.POST, request.FILES, instance=stu)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Updated Successfully!")
            return redirect('u-profileedit',pk=stu.id)  
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            department = Department.objects.all()
            context = {
                'form': form,
                'student': stu,
                'department': department
            }
            return render(request, self.template_name, context)

class EventView(TemplateView):
    template_name = "events.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        event = Event.objects.all()
        context['event'] =event
        return context

class NotificationView(TemplateView):
    template_name = "notifications.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['notification'] = Notification.objects.all()
        return context