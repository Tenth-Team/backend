from django.contrib import admin

from .models import Content, Ambassador, TrainingProgram, AmbassadorGoal


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AmbassadorGoal)
class AmbassadorGoalAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'country',
                    'city', 'status', 'reg_date')
    list_filter = ('gender', 'country', 'city', 'status', 'reg_date')
    search_fields = ('full_name', 'country', 'city', 'email', 'phone_number')
    filter_horizontal = ('amb_goal',)
