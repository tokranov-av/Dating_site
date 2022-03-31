from django.contrib import admin
from .models import User, LikedUsers


@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'avatar',
        'gender', 'latitude', 'longitude', 'is_active',
        'is_staff', 'is_superuser',
    )
    list_display_links = ('id', 'email')
    ordering = ('id',)
    readonly_fields = ('date_joined',)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        'email', 'first_name', 'last_name', 'avatar',
                        'gender', 'latitude', 'longitude', 'is_active',
                        'is_staff', 'is_superuser', 'password'
                    )
                ),
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(LikedUsers)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'liked_user', 'send_email')
    ordering = ('id',)
    list_display_links = ('id',)
