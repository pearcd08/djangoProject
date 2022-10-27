from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.urls import reverse, reverse_lazy


# Create your models here.
class Student(models.Model):
    student_id = models.AutoField(validators=[MinValueValidator(1000000), MaxValueValidator(20000000)],
                                  primary_key=True)
    dob = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('student-list')


class Lecturer(models.Model):
    lecturer_id = models.AutoField(validators=[MinValueValidator(20000001), MaxValueValidator(30000000)],                                   primary_key=True)
    dob = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Course(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('course-list')

class Semester(models.Model):

    year = models.CharField(max_length=4)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name + " " + self.year

    def get_absolute_url(self):
        return reverse('semester-list')


class Class(models.Model):
    number = models.CharField(max_length=6)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True, null=True, related_name="enrolled_student")

    def __str__(self):
        return self.number +": "+self.course.__str__()

    def get_absolute_url(self):
        return reverse('class-list')



class CollegeDay(models.Model):
    collegedate = models.DateField()
    collegeclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True, null=True, related_name="collegeday_student")


    def __str__(self):
        return self.collegedate.strftime('%m/%d/%Y')

