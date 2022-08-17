from django.urls import path

from subject import views

urlpatterns = [
    #-------------------------Mark-------------------------#
    
    path(
        'mark/',
        views.MarkListCreateAPIView.as_view(),
        name='mark'
    ),

    path(
        'mark/detail/<int:pk>',
        views.MarkRetrieveUpdateDestroyAPIView.as_view(),
        name='mark_detail'
    ),
    
    #-------------------------Quarter-------------------------#

    path(
        'quarter/',
        views.QuarterListCreateAPIView.as_view(),
        name='quarter'
    ),

    path(
        'quarter/detail/<int:pk>',
        views.QuarterRetrieveUpdateDestroyAPIView.as_view(),
        name='quarter_detail'
    ),

    #-------------------------Diary-------------------------#

    path(
        'diary/',
        views.DiaryListAPIView.as_view(),
        name='diary'
    ),

    path(
        'diary/detail/<int:pk>',
        views.DiaryRetrieveAPIView.as_view(),
        name='diary_detail'
    ),

    #-------------------------TimeTable-------------------------#

    path(
        'timetable/',
        views.TimeTableListCreateAPIView.as_view(),
        name='timetable'
    ),

    path(
        'timetable/detail/<int:pk>',
        views.TimeTableRetrieveUpdateDestroyAPIView.as_view(),
        name='timetable_detail'
    ),

    #-------------------------Course-------------------------#

    path(
        'course/',
        views.CourseListCreateAPIView.as_view(),
        name='course'
    ),

    path(
        'course/detail/<int:pk>',
        views.CourseRetrieveUpdateDestroyAPIView.as_view(),
        name='course_detail'
    ),

]