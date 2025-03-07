from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(CustomUser)
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
