import re
from turtle import pd

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from attendance import models
from attendance.forms import ClassForm, CourseForm, UserForm, SemesterForm
from attendance.models import Lecturer, Class, Student, Course, Semester, CollegeDay


# Create your views here.
def home(request):
    return render(request, "home.html")


class HomeView(ListView):
    model = Class
    template_name = "home.html"


# Students
class ListStudent(ListView):
    model = Student
    template_name = "student/student-list.html"

class ListLecturer(ListView):
    model = Lecturer
    template_name = "lecturer/lecturer-list.html"


class LecturerDetailView(DetailView):
    model = Lecturer
    template_name = "lecturer/lecturer-detail.html"


class UpdateLecturerView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "reusable/update-reusable.html"
    success_url = reverse_lazy('lecturer-list')


class DeleteLecturerView(DeleteView):
    model = User
    template_name = "reusable/delete-reusable.html"
    success_url = reverse_lazy('lecturer-list')


# Classes
class ListClass(ListView):
    model = Class
    template_name = "class/class-list.html"


class AddClassView(CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'reusable/add-reusable.html'


class UpdateClassView(UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "reusable/update-reusable.html"


class DeleteClassView(DeleteView):
    model = Class
    template_name = "reusable/delete-reusable.html"
    success_url = reverse_lazy('class-list')


# Courses
class ListCourse(ListView):
    model = Course
    template_name = "course/course-list.html"


class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course-detail.html"


class AddCourseView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'reusable/add-reusable.html'


class UpdateCourseView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "reusable/update-reusable.html"


class DeleteCourseView(DeleteView):
    model = Course
    template_name = "reusable/delete-reusable.html"
    success_url = reverse_lazy('course-list')


# Semesters
class ListSemester(ListView):
    model = Semester
    template_name = "semester/semester-list.html"


class AddSemesterView(CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'reusable/add-reusable.html'


class UpdateSemesterView(UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = "reusable/update-reusable.html"


class DeleteSemesterView(DeleteView):
    model = Semester
    template_name = "reusable/delete-reusable.html"
    success_url = reverse_lazy('semester-list')


def studentDetail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student_classes = Class.objects.filter(students__student_id=student_id)
    percentage_classes = Class.objects.filter(students__student_id=student_id).values('id')

    classList = list(percentage_classes)
    percentageList = list()

    i = 0
    while i < len(classList):
        classtochange = str(classList[i])
        class_id = re.sub(r'[^0-9]', '', classtochange)
        total_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id)
        attended_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id, students=student_id)

        attendance_result = attended_collegedays.count() / total_collegedays.count()
        attendance_percentage = int(round(attendance_result * 100))
        percentageList.append(attendance_percentage)

        return render(request, "student/student-detail.html", {
            "student": student,
            "student_classes": student_classes,
            "percentages": percentageList

        })


def studentClassDetail(request, student_id, class_id):
    student = get_object_or_404(Student, student_id=student_id)
    selected_class = Class.objects.get(id=class_id)
    total_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id)
    attended_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id, students=student_id)

    attendance_result = attended_collegedays.count() / total_collegedays.count()
    attendance_percentage = int(round(attendance_result * 100))

    return render(request, "student/student-class-detail.html", {
        "student": student,
        "selected_class": selected_class,
        "attended_classes": total_collegedays,
        "percentage": attendance_percentage

    })


def deleteStudent(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, "student/delete-student.html", {
        "student": student
    })


def confirmDeleteStudent(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    user = get_object_or_404(User, id=student.user_id)
    student.delete()
    user.delete()
    return HttpResponseRedirect(reverse('student-list'))


def deleteLecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, lecturer_id=lecturer_id)
    return render(request, "lecturer/delete-lecturer.html", {
        "lecturer": lecturer
    })


def confirmDeleteLecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, lecturer_id=lecturer_id)
    user = get_object_or_404(User, id=lecturer.user_id)
    lecturer.delete()
    user.delete()
    return HttpResponseRedirect(reverse('lecturer-list'))


def CustomStudentRegistration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        dob = request.POST.get("dob")

        if username == "" or firstname == "" or lastname == "" or dob == "":
            return render(request, "reusable/register-reusable.html", {
                "message": "Please enter all fields",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "dob": dob,
            })

        if password1 == password2 and password1 != "":
            user = User.objects.create_user(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            user.save()
            student = Student(user=user)
            student.dob = dob
            user.groups.add(1)
            student.save()

            return HttpResponseRedirect(reverse('student-list'))
        else:
            return render(request, "reusable/register-reusable.html", {
                "passwordmessage": "Passwords are not same",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "dob": dob,
            })
    return render(request, "reusable/register-reusable.html")


def updateStudentRegistration(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username == "" or firstname == "" or lastname == "":
            return render(request, "reusable/update-registration-reusable.html", {
                "message": "Fields cannot be blank",
                "student": student
            })

        if password1 == "" and password2 == "":
            user = User.objects.get(username__exact=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()
            return HttpResponseRedirect(reverse('student-list'))

        elif password1 == password2:
            user = User.objects.get(username__exact=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            user.save()

            return HttpResponseRedirect(reverse('student-list'))
        else:
            return render(request, "reusable/update-registration-reusable.html", {
                "passwordmessage": "Passwords are not same",
                "student": student
            })
    return render(request, "reusable/update-registration-reusable.html", {
        "student": student
    })


def studentAttendance(request):
    student_id = request.user.student.student_id
    student = get_object_or_404(Student, student_id=student_id)
    studentclasses = Class.objects.filter(students=student_id)
    attendedclasses = CollegeDay.objects.all

    return render(request, "student/student-attendance.html", {
        "current_student": student,
        "student_classes": studentclasses,
        "attended_classes": attendedclasses

    })


def studentAttendanceDetail(request, class_id):
    student_id = request.user.student.student_id
    student = get_object_or_404(Student, student_id=student_id)
    selected_class = Class.objects.get(id=class_id)
    total_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id)
    attended_collegedays = CollegeDay.objects.filter(collegeclass_id=class_id, students=student_id)

    attendance_result = attended_collegedays.count() / total_collegedays.count()
    attendance_percentage = str(round(attendance_result * 100)) + '%'

    return render(request, "student/student-attendance-detail.html", {
        "current_student": student,
        "selected_class": selected_class,
        "attended_classes": total_collegedays,
        "percentage": attendance_percentage

    })


def uploadStudents(request):
    if len(request.FILES) != 0:
        if request.method == "POST" and len(request.FILES["myfile"]) != 0:
            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            upload_file_url = fs.url(filename)
            excel_data = pd.read_excel(myfile)
            data = pd.DataFrame(excel_data)
            usernames = data["Username"].tolist()
            firstnames = data["First Name"].tolist()
            lastnames = data["Last Name"].tolist()
            emails = data["Email"].tolist()
            dobs = data["DOB"].tolist()
            failed_usernames = []
            success_usernames = []
            i = 0
            j = 0
            while i < len(usernames):
                if User.objects.filter(username=usernames[i]).exists():
                    username = usernames[i]
                    firstname = firstnames[i]
                    lastname = lastnames[i]
                    password = str(dobs[i]).split(" ")[0].replace("-", "")
                    failed_usernames.append(
                        firstname + " " + lastname + " - Username: " + username + " Password:" + password)
                    i = i + 1

                else:
                    username = usernames[i]
                    firstname = firstnames[i]
                    lastname = lastnames[i]
                    email = emails[i]
                    password = str(dobs[i]).split(" ")[0].replace("-", "")
                    dob = dobs[i]
                    user = User.objects.create_user(username=username)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.email = email
                    user.set_password(password)
                    user.save()
                    student = Student(user=user)
                    student.dob = dob
                    user.groups.add(1)
                    student.save()
                    user.save()
                    i = i + 1
                    j = j + 1
                    success_usernames.append(firstname + " " + lastname + " - " + password)

            if j == len(usernames):
                return render(request, 'student/student_upload.html', {
                    "upload_file_url": upload_file_url,
                    "successmessage": "All Students Successfully Uploaded!",
                    "success_usernames": success_usernames

                })
            elif 0 < j < len(usernames):
                return render(request, 'student/student_upload.html', {
                    "upload_file_url": upload_file_url,
                    "failmessage": "Some students couldn't be uploaded",
                    "failed_usernames": failed_usernames,
                    "success_usernames": success_usernames
                })
            elif j == 0:
                return render(request, 'student/student_upload.html', {
                    "upload_file_url": upload_file_url,
                    "failmessage": "No Students could be uploaded",
                    "failed_usernames": failed_usernames
                })
    else:
        return render(request, 'student/student_upload.html', {
            "filemessage": "Select a file!",

        })

    return render(request, 'student/student_upload.html')


# Lecturers



def AddCollegeDay(request):
    class_id = request.POST.get("class_id")
    selected_class = Class.objects.get(id=class_id)
    newdate = request.POST.get("date")
    if newdate != "":
        college_day = CollegeDay(collegedate=newdate, collegeclass_id=class_id)
        college_day.save()
        return HttpResponseRedirect(reverse('class-detail', args=[str(class_id)]))
    else:

        return render(request, "class/class-detail.html", {
            "datemessage": "Select a date!",
            "class": selected_class
        })


def RemoveCollegeDay(request, collegeday_id):
    selected_collegeday = get_object_or_404(CollegeDay, id=collegeday_id)
    class_id = selected_collegeday.collegeclass.id
    selected_collegeday.delete()
    return HttpResponseRedirect(reverse('class-detail', args=[str(class_id)]))


import pandas as pd


def ClassDetail(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.all()
    context = {"class": selected_class,
               "students": students}
    return render(request, 'class/class-detail.html', context)


def enrolStudent(request, class_id, student_id):
    selected_class = get_object_or_404(Class, id=class_id)
    selected_student = get_object_or_404(Student, student_id=student_id)

    selected_class.students.add(selected_student)
    return HttpResponseRedirect(reverse('class-detail', args=[class_id]))


def withdrawStudent(request, class_id, student_id):
    selected_class = get_object_or_404(Class, id=class_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_class.students.remove(selected_student)
    return HttpResponseRedirect(reverse('class-detail', args=[class_id]))


def collegeDayDetail(request, collegeday_id):
    selected_collegeday = get_object_or_404(CollegeDay, id=collegeday_id)
    students = selected_collegeday.collegeclass.students.all()
    context = {"collegeday": selected_collegeday,
               "students": students}
    return render(request, 'collegeday/collegeday-detail.html', context)


def markAsPresent(request, collegeday_id, student_id):
    selected_collegeday = get_object_or_404(CollegeDay, id=collegeday_id)
    selected_student = get_object_or_404(Student, student_id=student_id)

    selected_collegeday.students.add(selected_student)
    return HttpResponseRedirect(reverse('collegeday-detail', args=[collegeday_id]))


def markAsAbsent(request, collegeday_id, student_id):
    selected_collegeday = get_object_or_404(CollegeDay, id=collegeday_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_collegeday.students.remove(selected_student)
    return HttpResponseRedirect(reverse('collegeday-detail', args=[collegeday_id]))


def lecturerDetail(request, lecturer_id):
    selected_lecturer = get_object_or_404(Lecturer, lecturer_id=lecturer_id)

    classes = Class.objects.filter(lecturer_id=None)
    context = {"lecturer": selected_lecturer,
               "availableclass": classes}
    return render(request, 'lecturer/lecturer-detail.html', context)


def assignLecturer(request, class_id, lecturer_id):
    Class.objects.filter(id=class_id).update(lecturer=lecturer_id)
    return HttpResponseRedirect(reverse('lecturer-detail', args=[lecturer_id]))


def withdrawLecturer(request, class_id, lecturer_id):
    Class.objects.filter(id=class_id).update(lecturer=None)
    return HttpResponseRedirect(reverse('lecturer-detail', args=[lecturer_id]))


def semesterDetail(request, semester_id):
    selected_semester = get_object_or_404(Semester, id=semester_id)
    assignedclasses = Class.objects.filter(semester_id=semester_id)
    context = {"semester": selected_semester,
               "assignedclasses": assignedclasses

               }
    return render(request, 'semester/semester-detail.html', context)


def addSemester(request):
    if request.method == "POST":
        year = request.POST.get("year")
        name = request.POST.get("name")
        if name == "" or year == "":
            return render(request, "semester/add-semester.html", {
                "message": "Please Enter All Fields",
            })

        elif Semester.objects.filter(year=year, name=name).count() != 0:
            return render(request, "semester/add-semester.html", {
                "message": "Semester Already Exists",
            })

        else:
            Semester.objects.create(year=year, name=name)
            return HttpResponseRedirect(reverse('semester-list'))

    return render(request, "semester/add-semester.html")


def CustomLecturerRegistration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        dob = request.POST.get("dob")

        if username == "" or firstname == "" or lastname == "" or dob == "":
            return render(request, "reusable/register-reusable.html", {
                "message": "Please enter all fields",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "dob": dob,
            })

        if password1 == password2 and password1 != "":
            user = User.objects.create_user(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            user.save()
            lecturer = Lecturer(user=user)
            lecturer.dob = dob
            user.groups.add(2)
            lecturer.save()

            return HttpResponseRedirect(reverse('lecturer-list'))
        else:
            return render(request, "reusable/register-reusable.html", {
                "passwordmessage": "Passwords are not same",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "dob": dob,
            })
    return render(request, "reusable/register-reusable.html")


def updateLecturerRegistration(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, lecturer_id=lecturer_id)
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username == "" or firstname == "" or lastname == "":
            return render(request, "reusable/update-registration-reusable.html", {
                "message": "Fields cannot be blank",
                "lecturer": lecturer
            })

        if password1 == password2:
            user = User.objects.get(username__exact=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            user.save()

            return HttpResponseRedirect(reverse('student-list'))
        else:
            return render(request, "reusable/update-registration-reusable.html", {
                "passwordmessage": "Passwords are not same",
                "lecturer": lecturer
            })
    return render(request, "reusable/update-registration-reusable.html", {
        "lecturer": lecturer
    })


def emailStudent(request, student_id, class_id):
    student = get_object_or_404(Student, student_id=student_id)
    studentuser = get_object_or_404(User, id=student.user_id)
    studentemail = studentuser.email
    selected_class = get_object_or_404(Class, id=class_id)
    if request.method == "POST":
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        sender_email = "gabriel_sl19798@hotmail.com"
        try:
            send_mail(subject, body, sender_email, [studentemail], fail_silently=False)
            return render(request, "student/email-student.html", {
                "message": "email has been sent to " + student.__str__(),
                "student": student,
                "studentemail": studentemail,
                "class": selected_class
            })
        except:
            return render(request, "student/email-student.html", {
                "message": "Email failed to send",
                "student": student,
                "studentemail": studentemail,
                "class": selected_class
            })
    return render(request, "student/email-student.html", {
        "student": student,
        "studentemail": studentemail,
        "class": selected_class
    })
