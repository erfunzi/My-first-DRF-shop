from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TwoFactorCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'mobile_number', 'first_name', 'last_name', 'is_staff', 'wallet_balance')

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('username', 'email', 'mobile_number', 'first_name', 'last_name', 'national_code')

    list_editable = ('is_staff',)

    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'mobile_number', 
                                     'birth_date', 'national_code', 'profile_picture', 'job')}),
        ('امکانات مالی', {'fields': ('wallet_balance', 'invite_code')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile_number', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

@admin.register(TwoFactorCode)
class TwoFactorCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'code')

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True 
    is_valid.short_description = 'معتبر؟'