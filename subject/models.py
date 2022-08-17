from django.db import models

from account.models import Grade, School, SubWithTeach, Subject, Teacher, Student


class Diary(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='my_diary',
        verbose_name='Ученик(ца)'
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    
    def __str__(self) -> str:
        return f"Дневник {self.student}"
    
    class Meta:
        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'


class Mark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Кому',
        help_text='Ученик'
    )
    
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name='marks',
        verbose_name='Дневник',
    )

    subwithteach = models.ForeignKey(
        SubWithTeach,
        on_delete=models.SET_NULL,
        related_name='my_set_marks',
        verbose_name='Учитель с предметом',
        null=1,
    )
    
    mark = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        blank=1,
        null=1
    )
    
    why = models.CharField(
        max_length=255,
        verbose_name='За что',
        blank=1,
        null=1,
        help_text='Необязательно'
    )

    set_day = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создание'
    )

    def __str__(self) -> str:
        return f"Mark {self.student} to {self.mark}"
    
    def save(self, *args, **kwargs):
        self.diary = self.student.my_diary
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Quarter(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Кому',
        help_text='Ученик',
        related_name='my_quarters',
    )
    
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name='quarters',
        verbose_name='Дневник',
    )

    subwithteach = models.ForeignKey(
        SubWithTeach,
        on_delete=models.SET_NULL,
        related_name='my_set_quarters',
        verbose_name='Учитель с предметом',
        null=1,
    )

    which_quarter = models.PositiveSmallIntegerField(
        verbose_name='Какой четверть',
        help_text='Цифрами',
    )

    mark = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
    )
    
    set_day = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создание'
    )

    def __str__(self) -> str:
        return f"{self.student} - {self.mark} за {self.which_quarter}"

    def save(self, *args, **kwargs):
        self.diary = self.student.my_diary
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Четверть'
        verbose_name_plural = 'Четверти'


class TimeTable(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='school_timetables',
        verbose_name='Школа',
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='our_timetables',
        verbose_name='Класс',
    )

    weekday = models.IntegerField(
        verbose_name='День недели',
        help_text='от 1 до 8',
    )

    subwithteach = models.ForeignKey(
        SubWithTeach,
        on_delete=models.SET_NULL,
        related_name='my_timetables',
        verbose_name='Учитель с предметом',
        null=1,
    )

    start_lesson = models.TimeField(
        verbose_name='Начало урока',
    )

    finish_lesson = models.TimeField(
        verbose_name='Конец урока',
    )

    def __str__(self) -> str:
        return f"{self.grade} - {self.weekday}"
    
    class Meta:
        verbose_name = 'Расписания'
        verbose_name_plural = 'Расписание'


class Course(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='school_course',
        verbose_name='Школа',
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name='my_course',
        verbose_name='Преподователь',
        null=1,
    )

    start_course = models.TimeField(
        verbose_name='Начало курса',
    )

    finish_course = models.TimeField(
        verbose_name='Конец курса',
    )

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=1,
        null=1,
        help_text='Необязательно',
    )
    
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        blank=1, 
        null=1,
        help_text='Необязательно',
    )

    weekdays = models.CharField(
        max_length=7,
        default='123',
        verbose_name='Какие дни будут',
        help_text='от 1 до 8',
    )    
    
    students = models.ManyToManyField(
        Student,
        related_name='my_course',
        blank=1,
        verbose_name='Ученики',
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = verbose_name + 'ы'

    
class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Ученик',
        related_name='my_attendants',
    )

    arrived = models.BooleanField(
        verbose_name='Прибыл(а)',
        default=True,
    )

    cause = models.CharField(
        max_length=250,
        verbose_name='Причина',
        help_text='Необязательно',
        null=1,
        blank=1,
    )

    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата',
    )

    def __str__(self) -> str:
        return f"Прибытия {self.student}"
    
    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = verbose_name
    


    


