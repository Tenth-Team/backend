from django.contrib import admin

from .models import (
    Ambassador,
    AmbassadorGoal,
    City,
    Content,
    Country,
    Merchandise,
    MerchandiseShippingRequest,
    TrainingProgram,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


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
    filter_horizontal = ('amb_goals',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'telegram', 'link', 'guide', 'status',)


@admin.register(Merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(MerchandiseShippingRequest)
class MerchandiseShippingRequestAdmin(admin.ModelAdmin):
    list_display = ('name_merch', 'ambassador', 'status_send',
                    'created_date', 'comment',)
