from rest_framework import serializers

from subject import models

SM = serializers.ModelSerializer

class MarkSerializer(SM):
    class Meta:
        model = models.Mark
        fields = '__all__'


class QuarterSerializer(SM):
    class Meta:
        model = models.Quarter
        fields = '__all__'


class DiarySerializer(SM):
    class Meta:
        model = models.Diary
        fields = '__all__'


class TimeTableSerializer(SM):
    class Meta:
        model = models.TimeTable
        fields = '__all__'






