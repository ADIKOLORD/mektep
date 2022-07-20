from rest_framework import generics, permissions, response
from django.contrib.auth import login, logout, authenticate

from account import models, serializers, utils
from account.permissions import IsUserDirector, \
    IsAuthorOrTeacher, IsTeacherOrReadOnly, IsTeacherAuthor, \
        IsTeacherAuthorOfGradeOrReadOnly as ITAOGORO

RUDAPIView = generics.RetrieveUpdateDestroyAPIView


#-----------------------------School-----------------------------+#


class SchoolRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserDirector]


#-----------------------------Teacher-----------------------------+#


class TeacherListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserDirector]

    def get(self, request, *args, **kwargs):
        school = request.user.teacher.school
        teacher = self.get_queryset().filter(school=school)
        serializer = serializers.TeacherSerializer(teacher, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        try:
            gen_user = utils.generate_name_password(models.User)
            user = models.User.objects.create(username=gen_user['username'])
            user.set_password(gen_user['password'])
            user.save()
            pk = request.user.teacher.school.pk
            school = models.School.objects.get(pk=pk)
            fullname = str(request.data['fullname'])
            gender = str(request.data['gender']).upper()
            position = request.data['position']
            email = request.data['email']
            
            teacher = models.Teacher.objects.create(
                user=user,
                fullname=fullname,
                school=school,
                gender=gender,
                position=position,
                email=email)
            
            data = {
                "id": teacher.id,
                "fullname": teacher.fullname,
                "username": gen_user['username'],
                "password": gen_user['password'],

                }
            
            utils.send_password_to_email(
                gen_user,
                teacher.fullname,
                teacher.email)
            
            return response.Response(data, status=201)
        
        except:
            return response.Response("Что-то не так!", status=400)


class TeacherRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherAuthor]


#-----------------------------Student-----------------------------+#


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        students = models.Student.objects.all()
        try:
            user = request.user.student
            s = students.filter(grade=user.grade)
        except:
            user = request.user.teacher
            s = students.filter(grade__classroom_teacher=user)
        serializer = serializers.StudentSerializer(s, many=1)
        return response.Response(serializer.data, status=200)
    
    def post(self, request, *args, **kwargs):
        try:
            gen_user = utils.generate_name_password(models.User)
            user = models.User.objects.create(username=gen_user['username'])
            user.set_password(gen_user['password'])
            user.save()
            pk = request.user.teacher.school.pk
            request.data['school'] = pk
            request.data['user'] = user.pk
            full_name = f"{request.data['surname']} {request.data['name']}"
            get_post = super().post(request, *args, **kwargs)
            utils.send_password_to_email(
                gen_user,
                full_name,
                request.data['email'])
            return get_post
        
        except:
            return response.Response("Что-то не так!", status=400)


class StudentRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrTeacher]


#-----------------------------Grade-----------------------------+#


class GradeListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            school = request.user.teacher.school
        
        except:
            school = request.user.student.school
        grades = self.get_queryset().filter(school=school)
        serializer = serializers.GradeSerializer(grades, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        try:
            wclass = request.data['which_class']
            class_teacher = request.user.teacher
            school = class_teacher.school
            
            grade = models.Grade.objects.create(
                which_class=wclass,
                classroom_teacher=class_teacher,
                school=school,
            )
            serializer = serializers.GradeSerializer(grade)
            return response.Response(serializer.data, status=201)
        
        except:
            return response.Response("Что-то пошло не так!", status=400)


class GradeRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ITAOGORO]


#-----------------------------Subject------------------------------+#


class SubjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            school = request.user.teacher.school
        
        except:
            school = request.user.student.school
        subjects = self.get_queryset().filter(school=school)
        serializer = serializers.SubjectSerializer(subjects, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['school'] = request.user.teacher.school.id
        return super().post(request, *args, **kwargs)
        

class SubjectRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]


#-----------------------------User------------------------------#


class UserAuthorizationAPIView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return response.Response("Успешно вошли!", status=201)
        
        return response.Response("Данные неправильны!", status=400)


class UserChangePasswordAPIView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        # this must be logic for change password
        return super().post(request, *args, **kwargs)


class UserLogoutAPIView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserAuthenticationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return response.Response("Вы вышли из системы!")

