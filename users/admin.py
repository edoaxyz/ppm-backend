from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_staff", "is_superuser", "date_joined")

