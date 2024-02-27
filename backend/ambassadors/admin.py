from django.contrib import admin
from .models import Ambassador, TrainingProgram, AmbassadorGoal
@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    pass

@admin.register(TrainingProgram)
class AmbassadorAdmin(admin.ModelAdmin):
    pass

@admin.register(AmbassadorGoal)
class AmbassadorAdmin(admin.ModelAdmin):
    pass