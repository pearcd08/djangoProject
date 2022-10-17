from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.IntegerField (validators=[MinValueValidator(1000000), MaxValueValidator(9999999)], primary_key = True)
    dob = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Lecturer(models.Model):
    lecturer_id = models.IntegerField(validators=[MinValueValidator(1000000), MaxValueValidator(9999999)], primary_key=True)
    dob = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Semester(models.Model):
    # drop down for years
    year = models.CharField(max_length=9)
    # drop down 1,2,3
    semester = models.CharField(max_length=20)

    def __str__(self):
        return self.semester + " " + self.year


class Course(models.Model):
    # drop down for years
    code = models.CharField(max_length=9)
    # drop down 1,2,3
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Class(models.Model):
    number = models.CharField(max_length=6)
    time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)


    def __str__(self):
        return "Class Number: "+self.number + " Time: " +self.time



class CollegeDay(models.Model):
    # drop down for years
    date = models.DateField()
    # drop down 1,2,3
    collegeclass = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.date + " - " + self.collegeclass















