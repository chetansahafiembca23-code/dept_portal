from django.contrib import admin
from .models import MonthlyNewspaper, Achievement,SliderImage,Faculty

@admin.register(MonthlyNewspaper)
class MonthlyNewspaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'month_year', 'uploaded_at')
    list_filter = ('month_year',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'title', 'date_awarded')
    search_fields = ('student_name', 'title')

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')



@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department')