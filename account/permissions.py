from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserDirector(BasePermission):
    """
    Проверяет Директор ли User
    """
    message = 'Только директора могут создать!'
    
    def has_permission(self, request, view):
        try:
            position = request.user.teacher.position
            return bool(str(position).lower() == 'директор')
        except:
            return False


class IsUserMinister(BasePermission):
    """
    Проверяет Министр ли User в своем классе
    """
    message = 'Только министрам класса разрешено'

    def has_permission(self, request, view):
        try:
            return bool(request.user.student.is_minister)
        except:
            return False


class IsAuthorOrTeacher(BasePermission):
    """
    Проверка автор ли User или Классный руководитель
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user == obj.user:
            "Если он автор то может обновить"
            return request.method == "PUT"
        try:
            return bool(request.user.teacher.grade == obj.user.student.grade)
        
        except:
            return False


class IsTeacherOrReadOnly(BasePermission):
    """
    Проверяет если учитель то можно создать
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        try:
            return bool(request.user.teacher)
        except:
            return False


class IsTeacherDetailOrReadOnly(BasePermission):
    """
    Проверяет если учитель то можно создать
    """
    
    def has_object_permission(self, request, view, obj):
        try:
            user = request.user.teacher
        except:
            user = request.user.student
        if user.school == obj.school:
            if request.method in SAFE_METHODS:
                return True
            try:
                return bool(request.user.teacher)
            except:
                return False
        return False


class IsTeacherAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user


class IsTeacherAuthorOfGradeOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return request.user.teacher == obj.classroom_teacher
        except:
            return False

