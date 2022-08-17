from django.contrib import admin

from account import models

@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_place', 'get_count', 'create_date']
    list_display_links = list_display[:-2]
    list_filter = ['create_date']
    save_on_top = True
    readonly_fields = ['description']
    search_fields = ['title', 'description', 'region', 'city']

    def get_count(self, obj):
        return f"{obj.quantity_teachers} | {obj.quantity_students}"

    def get_place(self, obj):
        if obj.village:
            return f"{obj.region} -> {obj.city} -> {obj.village}"
        return f"{obj.region} -> {obj.city}"

    get_count.short_description = "Кол-во T/S"
    get_place.short_description = "Местоположение"


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['school', 'fullname', 'position','create_date']
    list_display_links = list_display[:-1]
    list_filter = ['school', 'gender', 'create_date']
    save_on_top = True
    search_fields = ['school', 'fullname', 'email']


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['school', 'fullname', 'position','create_date']
    list_display_links = list_display[:-1]
    list_filter = ['school', 'gender', 'create_date']
    save_on_top = True
    search_fields = ['school__title', 'name', 'surname', 'patronymic', 'email']

    def fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['school', 'which_class', 'progress']
    list_display_links = list_display
    list_filter = ['school', 'create_date']
    readonly_fields = ['subjects']


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['school', 'title', 'create_date']
    list_display_links = list_display[:-1]
    list_filter = ['school', 'title', ]
    save_on_top = True


