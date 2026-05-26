from django.contrib import admin
from .models import Course, Group, Schedule, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'course')
    filter_horizontal = ('students',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject', 'day_of_week', 'start_time')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'value', 'date')
    list_filter = ('group', 'date')
