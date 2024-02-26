from django.contrib import admin

from .models import Content, Ambassador, TrainingProgram, AmbassadorGoal

# Register your models here.
admin.site.register(Content)
admin.site.register(Ambassador)
admin.site.register(TrainingProgram)
admin.site.register(AmbassadorGoal)
