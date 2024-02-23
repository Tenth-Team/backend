from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение модели User в админке."""

    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "patronymic",
        "email",
        "phone_number",
    )
