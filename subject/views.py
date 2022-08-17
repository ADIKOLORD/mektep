from rest_framework import generics, response, permissions as rper

from subject import models, serializers, permissions
from account import permissions as a_per

RUDAPIView = generics.RetrieveUpdateDestroyAPIView
IA = rper.IsAuthenticated

#-----------------------------Mark-----------------------------+#


class MarkListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Mark.objects.all()
    serializer_class = serializers.MarkSerializer
    permission_classes = [IA, a_per.IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если это учитель то все оценки который он поставил"""
            marks = models.Mark.objects.filter(teacher=user.teacher)
            serializer = serializers.MarkSerializer(marks, many=1)
        
        except:
            """Если это учиник то все оценки который он получил"""
            marks = models.Mark.objects.filter(student=user.student)
            serializer = serializers.MarkSerializer(marks, many=1)  
        
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['teacher'] = request.user.teacher.pk
        s = models.Student.objects.get(pk=request.data['student'])
        request.data['diary'] = s.my_diary.pk
        return super().post(request, *args, **kwargs)


class MarkRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Mark.objects.all()
    serializer_class = serializers.MarkSerializer
    permission_classes = [IA, permissions.IsTeacherAuthorOfMark]


#-----------------------------Quarter-----------------------------+#


class QuarterListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Quarter.objects.all()
    serializer_class = serializers.QuarterSerializer
    permission_classes = [IA, a_per.IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если он ученик то все четверти который получил"""
            quarters = self.get_queryset().filter(student=user.student)
        except:
            """Если он учитель то все четверти который поставил"""
            quarters = self.get_queryset().filter(teacher=user.teacher)
        serializer = serializers.QuarterSerializer(quarters, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['teacher'] = request.user.teacher.pk
        s = models.Student.objects.get(pk=request.data['student'])
        request.data['diary'] = s.my_diary.pk
        return super().post(request, *args, **kwargs)


class QuarterRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Quarter.objects.all()
    serializer_class = serializers.QuarterSerializer
    permission_classes = [IA, permissions.IsTeacherAuthorOfQuarter]


#-----------------------------Diary-----------------------------+#


class DiaryListAPIView(generics.ListAPIView):
    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiarySerializer
    permission_classes = [IA,]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если он ученик то его дневник"""
            diary = self.get_queryset().filter(student=user.student)
        
        except:
            """Если он учитель то все дневники его класса"""
            diary = self.get_queryset().filter(student__grade__classroom_teacher=user.teacher)
        serializer = serializers.DiarySerializer(diary, many=1)
        return response.Response(serializer.data, status=200)


class DiaryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiarySerializer
    permission_classes = [IA, permissions.IsTeacherOrAuthorOfDiary]


#-----------------------------TimeTable-----------------------------+#


class TimeTableListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TimeTable.objects.all()
    serializer_class = serializers.TimeTableSerializer
    permission_classes = [IA, a_per.IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если ст"""
            tts = self.get_queryset().filter(grade=user.student.grade)
        except:
            """Если уч"""
            tts = self.get_queryset().filter(school=user.teacher.school)
        serializer = serializers.TimeTableSerializer(tts, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['school'] = request.user.teacher.school.pk
        return super().post(request, *args, **kwargs)


class TimeTableRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.TimeTable.objects.all()
    serializer_class = serializers.TimeTableSerializer
    permission_classes = [IA, a_per.IsTeacherDetailOrReadOnly]


#-----------------------------Course-----------------------------+#


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IA, a_per.IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если ст"""
            tts = self.get_queryset().filter(school=user.student.school)
        
        except:
            """Если уч"""
            tts = self.get_queryset().filter(school=user.teacher.school)
        serializer = serializers.CourseSerializer(tts, many=1)
        return response.Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['school'] = request.user.teacher.school.pk
        request.data['teacher'] = request.user.teacher.pk
        return super().post(request, *args, **kwargs)


class CourseRetrieveUpdateDestroyAPIView(RUDAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IA, a_per.IsTeacherDetailOrReadOnly]


#-----------------------------Attendance-----------------------------+#


class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [IA, a_per.IsTeacherOrReadOnly]

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            """Если студент то только свои посещаемости"""
            tts = self.get_queryset().filter(student=user.student)
        
        except:
            """Если учитель то посещаемость его класса"""
            try:
                t_grade = user.teacher.grade
                tts = self.get_queryset().filter(student__grade=t_grade)
            except:
                text = "Вы не ученик или классный руководитель :)"
                return response.Response(text, status=200)
        serializer = serializers.AttendanceSerializer(tts, many=1)
        return response.Response(serializer.data, status=200)


# need to change permissions classes
class AttendanceRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [IA, a_per.IsTeacherAuthorOfGradeOrReadOnly]


