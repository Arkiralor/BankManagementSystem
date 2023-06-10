from django.contrib import admin

from user_app.models import User, UserProfile, Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("id", "username", "email")
    ordering = ("-date_joined",)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "line_1", "line_2", "city", "district", "state", "country", "pin_code")
    search_fields = (
        "user__id",
        "user__username",
        "user__email",
        "line_1",
        "line_2",
        "city",
        "district",
        "state",
        "country",
        "pin_code"
    )
    raw_id_fields = ("user",)
    ordering = ("-created",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name")
    search_fields = (
        "first_name",
        "last_name",
        "user__id",
        "user__username",
        "user__email"
    )
    raw_id_fields = ("user",)
    ordering = ("-created",)
