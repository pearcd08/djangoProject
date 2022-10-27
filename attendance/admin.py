from django.contrib import admin

from attendance.models import Student, Lecturer, Semester, Class, Course, CollegeDay

# Register your models here.

admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(CollegeDay)
# admin.site.register(Enrollment)
# admin.site.register(Attendance)