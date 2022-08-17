# Generated by Django 4.0.6 on 2022-07-29 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_subwithteach_alter_grade_subjects'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='quarter',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='quarter',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='teacher',
        ),
        migrations.AddField(
            model_name='mark',
            name='subwithteach',
            field=models.ForeignKey(null=1, on_delete=django.db.models.deletion.SET_NULL, related_name='my_set_marks', to='account.subwithteach', verbose_name='Учитель с предметом'),
            preserve_default=1,
        ),
        migrations.AddField(
            model_name='quarter',
            name='subwithteach',
            field=models.ForeignKey(null=1, on_delete=django.db.models.deletion.SET_NULL, related_name='my_set_quarters', to='account.subwithteach', verbose_name='Учитель с предметом'),
            preserve_default=1,
        ),
        migrations.AddField(
            model_name='timetable',
            name='subwithteach',
            field=models.ForeignKey(null=1, on_delete=django.db.models.deletion.SET_NULL, related_name='my_timetables', to='account.subwithteach', verbose_name='Учитель с предметом'),
            preserve_default=1,
        ),
        migrations.AlterField(
            model_name='quarter',
            name='mark',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Оценка'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrived', models.BooleanField(default=True, verbose_name='Прибыл(а)')),
                ('cause', models.CharField(blank=1, help_text='Необязательно', max_length=250, null=1, verbose_name='Причина')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_attendants', to='account.student', verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Посещаемость',
                'verbose_name_plural': 'Посещаемость',
            },
        ),
    ]
