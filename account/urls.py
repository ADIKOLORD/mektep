from django.urls import path

from account import views

urlpatterns = [
    #-------------------------School-------------------------#
    
    path(
        'school/detail/<int:pk>',
        views.SchoolRetrieveUpdateDestroyAPIView.as_view(),
        name='school_detail'
    ),

    #-------------------------Teacher-------------------------#

    path(
        'teacher/',
        views.TeacherListCreateAPIView.as_view(),
        name='teacher',
    ),

    path(
        'teacher/detail/<int:pk>',
        views.TeacherRetrieveUpdateDestroyAPIView.as_view(),
        name='teacher_detail'
    ),

    #-------------------------Student-------------------------#

    path(
        'student/',
        views.StudentListCreateAPIView.as_view(),
        name='student',
    ),

    path(
        'student/detail/<int:pk>',
        views.StudentRetrieveUpdateDestroyAPIView.as_view(),
        name='student_detail'
    ),

    #-------------------------Grade-------------------------#

    path(
        'grade/',
        views.GradeListCreateAPIView.as_view(),
        name='grade',
    ),

    path(
        'grade/detail/<int:pk>',
        views.GradeRetrieveUpdateDestroyAPIView.as_view(),
        name='grade_detail'
    ),

    #-------------------------Subject-------------------------#

    path(
        'subject/',
        views.SubjectListCreateAPIView.as_view(),
        name='subject',
    ),

    path(
        'subject/detail/<int:pk>',
        views.SubjectRetrieveUpdateDestroyAPIView.as_view(),
        name='subject_detail'
    ),

    #-------------------------User-------------------------#

    path(
        'authorization/',
        views.UserAuthorizationAPIView.as_view(),
        name='authorization',
    ),

    path(
        'change/password/',
        views.UserChangePasswordAPIView.as_view(),
        name='change_password'
    ),

    path(
        'logout/',
        views.UserLogoutAPIView.as_view(),
        name='logout'
    ),

]
