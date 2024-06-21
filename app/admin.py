from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from app.models import *


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email",
                    "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
         "fields": ("first_name", "last_name", "email","image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Order)