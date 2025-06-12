from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id","username", "full_name", "role","is_verified")
    list_filter = ("is_staff", "role","is_verified")
    fieldsets = (
        ("Authenticate", {"fields": ("username","full_name", "password","role","department","is_verified","is_staff")}),
        # (
        #     "Permissions",
        #     {
        #         "fields": (
        #             "is_staff",
        #             "is_active",
        #             "is_superuser",
        #             "is_verified",
        #         )
        #     },
        # ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Last login", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )
    search_fields = ("username","full_name")
    ordering = ("full_name","is_verified")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)