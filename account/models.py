from django.db import models

from django.contrib.auth.models import User


class School(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        unique=True,
    )

    description = models.TextField(
        verbose_name='Описание',
    )

    region = models.CharField(
        max_length=50,
        verbose_name='Область',
    )

    city = models.CharField(
        max_length=100,
        verbose_name='Город',
    )

    village = models.CharField(
        max_length=255,
        verbose_name='Село',
        help_text='Необязательно',
        blank=1,
        null=1,
    )

    quantity_students = models.PositiveIntegerField(
        verbose_name='Кол-во учеников',
        default=0,
    )

    quantity_teachers = models.PositiveIntegerField(
        verbose_name='Кол-во учителей',
        default=0,
    )

    create_date = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'
    

GENDER = (('M', 'MAN'), ('W', 'WOMAN'))
class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher',
        verbose_name='Пользователь'
    )
    
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name='Школа',
        related_name='teachers',
    )

    fullname = models.CharField(
        max_length=100,
        verbose_name='Полное имя',
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        verbose_name='Пол',
    )
    
    email = models.EmailField(
        unique=1,
        help_text='Для получение логина'
    )

    position = models.CharField(
        max_length=200,
        verbose_name='Должность',
    )

    image = models.ImageField(
        upload_to='photo/teachers/%m/%d',
        blank=1,
        null=1,
        verbose_name='Фото',
    )

    create_date = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return self.fullname

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

    class Meta:
        verbose_name = 'Учетель'
        verbose_name_plural = 'Учетеля'


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student',
        verbose_name='Пользователь'
    )
    
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name='Школа',
        related_name='students',
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )

    surname = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
    )

    patronymic = models.CharField(
        max_length=100,
        verbose_name='Отчество',
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        verbose_name='Пол',
    )
    
    email = models.EmailField(
        unique=1,
        help_text='Для получение логина'
    )

    grade = models.ForeignKey(
        'Grade',
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='Класс',
    )
    
    position = models.CharField(
        max_length=255,
        verbose_name='Должность',
        blank=1,
        null=1
    )

    is_minister = models.BooleanField(
        default=False,
        verbose_name='Министр'
    )

    phone_number = models.CharField(
        max_length=100,
        verbose_name='Номер телефона',
        help_text='Ученика',
    )

    fullname_father = models.CharField(
        max_length=255,
        verbose_name='Полное имя отца',
        blank=1,
        null=1,
    )

    phone_number_f = models.CharField(
        max_length=100,
        verbose_name='Телефон номер отца',
        blank=1,
        null=1
    )

    fullname_mother = models.CharField(
        max_length=255,
        verbose_name='Полное имя мамы',
        blank=1,
        null=1,
    )

    phone_number_m = models.CharField(
        max_length=100,
        verbose_name='Телефон номер мамы',
        blank=1,
        null=1
    )

    create_date = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return f"{self.surname} {self.name}"

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()


    class Meta:
        verbose_name = 'Ученик(ца)'
        verbose_name_plural = 'Ученики'


class Grade(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Школа',
    )
    
    classroom_teacher = models.OneToOneField(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name='Классный руководитель',
        related_name='grade',
    )
    
    which_class = models.CharField(
        max_length=5,
        verbose_name='Какой класс',
        help_text='Цифра и Буква',
    )

    progress = models.FloatField(
        default=100,
        verbose_name='Успеваемость',
        help_text='В процентах',
    )

    subjects = models.ManyToManyField(
        'Subject',
        related_name='use_grades',
        verbose_name='Предметы',
    )

    create_date = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return f"{self.classroom_teacher} - {self.which_class}"
    
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        unique_together = ['school', 'which_class']


class Subject(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='Школа',
    )
    
    title = models.CharField(
        max_length=100,
        verbose_name='Название предмета',
    )

    create_date = models.DateTimeField(
        auto_now_add=1,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.title = str(self.title).title()
        return super().save(*args, **kwargs)    

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        unique_together = ['school', 'title']

    