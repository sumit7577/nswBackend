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
         "fields": ("first_name", "last_name", "email","image","phone")}),
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

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","image","email","phone"),
            },
        ),
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_type', 'starting_date', 'ending_date', 'registration_fees', 'display_students')
    
    def display_students(self, obj):
        return ", ".join([student.username for student in obj.students.all()])
    
    display_students.short_description = 'Students'


class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('installment_number','course','date','price','display_students')
    
    def display_students(self, obj):
        return ", ".join([student.username for student in obj.user.all()])
    
    display_students.short_description = 'Students'

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Order)
admin.site.register(Installment,InstallmentAdmin)
admin.site.register(Sessions)