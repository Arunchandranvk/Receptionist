from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(CustomUser)