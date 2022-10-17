from django.contrib import admin

from attendance.models import Student, Lecturer

# Register your models here.

admin.site.register(Student)
admin.site.register(Lecturer)