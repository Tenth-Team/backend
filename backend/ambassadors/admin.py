from django.contrib import admin

from .models import Ambassador, AmbassadorGoal, Content, TrainingProgram


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


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
       'id', 'full_name', 'telegram', 'link', 'guide', 'status',
    )
