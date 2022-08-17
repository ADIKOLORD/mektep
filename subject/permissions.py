
from rest_framework.permissions import BasePermission


class IsTeacherAuthorOfMark(BasePermission):
    
    message = "Только автор или учитель могут видеть"

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.student == obj.student:
                return request.method == 'GET'
            return False
        
        except:
            return request.user.teacher == obj.teacher
        

class IsTeacherAuthorOfQuarter(BasePermission):
    
    message = "Только автор или учитель либо класс-рук. могут видеть"

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.student == obj.student:
                return request.method == 'GET'
            return False
        
        except:
            t = request.user.teacher
            teacher = t == obj.teacher
            class_teacher = t == obj.student.grade.classroom_teacher
            return teacher or class_teacher
        

class IsTeacherOrAuthorOfDiary(BasePermission):
    
    message = "Вы не автор или классный руководитель"

    def has_object_permission(self, request, view, obj):
        user = request.user
        student = obj.student
        try:
            return student == user.student
        except:
            return student.grade.classroom_teacher == user.teacher

