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
        event = Event.objects.all().order_by('-created_at')
        context['event'] = event
        return context

class NotificationView(TemplateView):
    template_name = "notifications.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['notification'] = Notification.objects.all().order_by('-created_at')
        return context
    
# class ExamFormView(View):
#     template_name = 'student_view.html'
    
#     def get(self, request, *args, **kwargs):
#         student = Student.objects.all()
#         count = student.count()
#         department = Department.objects.all()
#         context = {
#             'students':student,
#             'department':department,
#             'count':count
            
#         }
#         return render(request, self.template_name, context)
    
#     def post(self, request, *args, **kwargs):
#         form = StudentForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Student Added Successfully!")
#             return redirect('student')
#         else:
#             messages.error(request, "Failed. Please correct the errors below!")
#             students = Student.objects.all()
#             context = {
#                 'students': students,
#                 'form': form
#             }
#             return render(request, self.template_name, context)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML



class SemesterRegistrationView(View):
    template_name = "exam_form.html"

    def get(self, request, pk):
        return render(request, self.template_name)

    def post(self, request, pk):
        def get_value(field_name):
            """Returns None if the field is empty, else returns the field value."""
            return request.POST.get(field_name) or None

        # Get form data
        name = get_value("name")
        ktu_number = get_value("ktu_number")
        program = get_value("program")
        semester = get_value("semester")
        batch = get_value("batch")
        date = get_value("date")
        stu_mobile= get_value("student_mobile")
        parent_mobile= get_value("parent_mobile")

        semester_data = []
        for i in range(1, 8):  # Assuming semesters 1 to 7
            semester_data.append({
                "semester": get_value(f"semester_{i}"),
                "credits_earned": get_value(f"credits_{i}"),
                "sgpa": get_value(f"sgpa_{i}"),
                "courses_failed": get_value(f"failed_{i}")
            })

        course_data = []
        for i in range(1, 8):  # Assuming 7 courses
            course_data.append({
                "course_code": get_value(f"course_code_{i}"),
                "course_name": get_value(f"course_name_{i}"),
                "internal_mark": get_value(f"internal_{i}"),
                "attendance": get_value(f"attendance_{i}")
            })

        context = {
            "name": name,
            "ktu_number": ktu_number,
            "program": program,
            "semester": semester,
            "batch": batch,
            "date": date,
            "semester_data": semester_data,
            "course_data": course_data,
            "student_mobile":stu_mobile,
            "parent_mobile":parent_mobile
        }

        html_content = render_to_string("exam_form_pdf.html", context)

        pdf_file = HTML(string=html_content).write_pdf()
        pdf_filename = f"semester_registration_{ktu_number}.pdf"

        pdf_dir = os.path.join(settings.MEDIA_ROOT, "semester_pdfs")
        os.makedirs(pdf_dir, exist_ok=True) 
        pdf_path = os.path.join(pdf_dir, pdf_filename)

        with open(pdf_path, 'wb') as f:
            f.write(pdf_file)
        noti = get_object_or_404(Notification, id=pk)
        stu = get_object_or_404(Student, id=request.user.id)
        registration = SemesterRegistration(
            notification_id=noti,
            student=stu.std_id,
            pdf_file=f"semester_pdfs/{pdf_filename}" 
        )
        registration.save()
        messages.success(request, "Semester registration form submitted and saved as PDF successfully.")
        return redirect("u-notification")