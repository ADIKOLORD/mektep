from django.contrib import admin

from subject import models

admin.site.register(models.Attendance)
admin.site.register(models.Mark)
admin.site.register(models.Quarter)
admin.site.register(models.Diary)
admin.site.register(models.TimeTable)
admin.site.register(models.Course)
"""
class MarkInline(admin.TabularInline):
    model = models.Mark
    extra = 0
    readonly_fields = ['subwithteach', 'mark', 'set_day']
    exclude = ['student', 'why']
    ordering = ['-set_day']


class QuarterInline(admin.TabularInline):
    model = models.Quarter
    extra = 0
    readonly_fields = ['which_quarter', 'mark', 'set_day']
    exclude = ['subwithteach']
    ordering = ['-set_day']



@admin.register(models.Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'mark']
    list_display_links = list_display[:-1]
    list_filter = ['mark', 'set_day', ]
    save_on_top = True
    fieldsets = [
        ('Главные данные', 
        {'fields': ['student', 'mark']}),
        ('Не важные данные', 
        {'fields': ['subject', 'why',]})
    ]
    readonly_fields = ['teacher', 'student', 'subject']


@admin.register(models.Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'which_quarter', 'mark']
    list_display_links = list_display[:-1]
    list_filter = ['mark', 'set_day', 'which_quarter']
    save_on_top = True


@admin.register(models.Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ['get_school', 'student', 'create_date']
    list_display_links = list_display[:-1]
    list_filter = ['create_date']
    save_on_top = True
    readonly_fields = ['student']
    inlines = [
        MarkInline,
        QuarterInline,
    ]

    def get_school(self, obj):
        return obj.student.school
    
    get_school.short_description = 'Школа'


@admin.register(models.TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['school', 'grade', 'weekday']
    list_display_links = list_display[:-1]
    list_filter = ['school', 'grade', 'weekday']
    save_on_top = True


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['school', 'teacher', 'title', 'price']
    list_display_links = list_display[:-1]
    list_filter = ['school', 'create_date']
    save_on_top = True
    filter_horizontal = ['students']
    readonly_fields = [
        'school', 
        'teacher',
        'title', 
        'start_course',
        'finish_course',
        'description', 
        ]
    search_fields = [
        'title', 
        'description', 
    ]
"""





