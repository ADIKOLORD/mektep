from django.db import models

from account.models import Grade, School, Subject, Teacher, Student


class Mark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Кому',
        help_text='Ученик'
    )
    
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name='Преподователь',
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Предмет',
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
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Quarter(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Кому',
        help_text='Ученик'
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Предмет',
    )

    which_quarter = models.PositiveSmallIntegerField(
        verbose_name='Какой четверть',
        help_text='Цифрами',
    )

    mark = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        blank=1,
        null=1
    )
    
    set_day = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создание'
    )

    def __str__(self) -> str:
        return f"{self.student} - {self.mark} за {self.which_quarter}"

    class Meta:
        verbose_name = 'Четверть'
        verbose_name_plural = 'Четверти'


class Diary(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='my_diary',
        verbose_name='Ученик(ца)'
    )

    marks = models.ManyToManyField(
        Mark, 
        related_name='diary',
        verbose_name='Оценки',
        blank=1,
    )

    quarters = models.ManyToManyField(
        Quarter,
        related_name='diary',
        verbose_name='Четверти',
        blank=1
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

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        related_name='sub_timetable',
        verbose_name='Предмет',
        null=1,
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name='my_timetables',
        verbose_name='Преподователь',
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



        
    
    
    



