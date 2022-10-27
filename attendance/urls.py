from django.urls import path

from .views import HomeView, ListClass, AddClassView, UpdateClassView, DeleteClassView, ListCourse, \
    AddCourseView, CourseDetailView, UpdateCourseView, DeleteCourseView, \
    ListStudent, ListLecturer, \
    UpdateLecturerView, DeleteLecturerView, CustomStudentRegistration, CustomLecturerRegistration, \
    ListSemester, UpdateSemesterView, DeleteSemesterView, \
    AddCollegeDay, uploadStudents, \
    ClassDetail, enrolStudent, withdrawStudent, \
    collegeDayDetail, markAsPresent, markAsAbsent, withdrawLecturer, assignLecturer, lecturerDetail, semesterDetail, \
    addSemester, updateStudentRegistration, updateLecturerRegistration, studentAttendance, studentAttendanceDetail, \
    RemoveCollegeDay, emailStudent, deleteStudent, confirmDeleteStudent, deleteLecturer, \
    confirmDeleteLecturer, studentDetail, studentClassDetail

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Student URLS
    path('students/', ListStudent.as_view(), name="student-list"),
    path('add_student', CustomStudentRegistration, name='add-student'),
    path('student/<int:student_id>', studentDetail, name="student-detail"),
    path('student/<int:student_id>/<int:class_id>', studentClassDetail, name="student-class-detail"),
    path('student/<int:student_id>/update', updateStudentRegistration, name="update-student"),
    path('student/<int:student_id>/delete', deleteStudent, name="delete-student"),
    path('student/<int:student_id>/confirm_delete', confirmDeleteStudent, name="confirm-delete-student"),
    path("upload_students", uploadStudents, name="upload-students"),
    path("enrol_student/<int:class_id>/<int:student_id>", enrolStudent, name="enrol-student"),
    path("withdraw_student/<int:class_id>/<int:student_id>", withdrawStudent, name="withdraw-student"),
    path("student_attendance", studentAttendance, name="student-attendance"),
    path("student_attendance_detail/<int:class_id>", studentAttendanceDetail, name="student-attendance-detail"),
    path("student/<int:student_id>/<int:class_id>/email_student", emailStudent, name="email-student"),


    # Lecturer URLS
    path('lecturers/', ListLecturer.as_view(), name="lecturer-list"),
    path('add_lecturer', CustomLecturerRegistration, name='add-lecturer'),
    path('lecturer/<int:lecturer_id>', lecturerDetail, name="lecturer-detail"),
    path('lecturer/<int:lecturer_id>/update', updateLecturerRegistration, name="update-lecturer"),
    path('lecturer/<int:lecturer_id>/delete', deleteLecturer, name="delete-lecturer"),
    path('lecturer/<int:lecturer_id>/confirm_delete', confirmDeleteLecturer, name="confirm-delete-lecturer"),
    path('withdrawLecturer/<int:class_id>/<int:lecturer_id>', withdrawLecturer, name="withdraw-lecturer"),
    path('assignLecturer/<int:class_id>/<int:lecturer_id>', assignLecturer, name="assign-lecturer"),

    # Class URLS
    path('classes/', ListClass.as_view(), name="class-list"),
    path('add_class/', AddClassView.as_view(), name="add-class"),
    path('class/<int:class_id>', ClassDetail, name="class-detail"),
    path('class/<int:pk>/update', UpdateClassView.as_view(), name="update-class"),
    path('class/<int:pk>/delete', DeleteClassView.as_view(), name="delete-class"),


    # Course URLS
    path('courses/', ListCourse.as_view(), name="course-list"),
    path('add_course/', AddCourseView.as_view(), name="add-course"),
    path('course/<int:pk>', CourseDetailView.as_view(), name="course-detail"),
    path('course/<int:pk>/update', UpdateCourseView.as_view(), name="update-course"),
    path('course/<int:pk>/delete', DeleteCourseView.as_view(), name="delete-course"),

    # semester URLS
    path('semesters/', ListSemester.as_view(), name="semester-list"),
    path('add_semester/', addSemester, name="add-semester"),
    path('semester/<int:semester_id>', semesterDetail, name="semester-detail"),
    path('semester/<int:pk>/update', UpdateSemesterView.as_view(), name="update-semester"),
    path('semester/<int:pk>/delete', DeleteSemesterView.as_view(), name="delete-semester"),

    # collegeday URLS
    path('collegeday/<int:collegeday_id>', collegeDayDetail, name="collegeday-detail"),
    path('markAsPresent/<int:collegeday_id>/<int:student_id>', markAsPresent, name="mark-as-present"),
    path("markAsAbsent/<int:collegeday_id>/<int:student_id>", markAsAbsent, name="mark-as-absent"),
    path("add_collegeday/", AddCollegeDay, name="add-collegeday"),
    path("remove_collegeday/<int:collegeday_id>", RemoveCollegeDay, name="remove-collegeday"),
]
