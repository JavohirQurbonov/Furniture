from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPCode, TelegramLink


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'first_name', 'telegram_chat_id', 'is_staff', 'created_at')
    search_fields = ('phone', 'first_name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Ma\'lumot', {'fields': ('first_name', 'age', 'address', 'telegram_chat_id')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(OTPCode)
admin.site.register(TelegramLink)
