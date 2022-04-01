from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, LikedUsers


@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'get_html_avatar',
        'gender', 'latitude', 'longitude', 'is_active',
        'is_staff', 'is_superuser',
    )
    list_display_links = ('id', 'email')
    ordering = ('id',)
    readonly_fields = ('date_joined', 'get_html_avatar')
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        'email', 'first_name', 'last_name', 'get_html_avatar',
                        'avatar','gender', 'latitude', 'longitude', 'is_active',
                        'is_staff', 'is_superuser', 'password'
                    )
                ),
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')

    def get_html_avatar(self, instance):
        if instance.avatar:
            return mark_safe(f"<img src='{instance.avatar.url}' width=80>")

    get_html_avatar.short_description = "Аватарка"

    admin.site.site_title = 'Админ-панель сайта знакомств'
    admin.site.site_header = 'Админ-панель сайта знакомств'


@admin.register(LikedUsers)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'liked_user', 'send_email')
    ordering = ('id',)
    list_display_links = ('id',)
