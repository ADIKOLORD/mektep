from rest_framework import serializers

from account import models

SM = serializers.ModelSerializer

#-----------------------School-----------------------#


class SchoolSerializer(SM):
    class Meta:
        model = models.School
        fields = '__all__'


#-----------------------Teacher-----------------------#


class TeacherSerializer(SM):
    class Meta:
        model = models.Teacher
        fields = '__all__'


#-----------------------Student-----------------------#


class StudentSerializer(SM):
    class Meta:
        model = models.Student
        fields = '__all__'


#-----------------------Grade-----------------------#


class GradeSerializer(SM):
    
    class Meta:
        model = models.Grade
        fields = '__all__'


#-----------------------Subject-----------------------#


class SubjectSerializer(SM):
    class Meta:
        model = models.Subject
        fields = '__all__'


#-----------------------User-----------------------#


class UserAuthenticationSerializer(SM):
    class Meta:
        model = models.User
        fields = ['username', 'password']


class UserChangePasswordSerializer(SM):
    class Meta:
        model = models.User
        fields = ['first_name', 'username', 'email', 'password']








