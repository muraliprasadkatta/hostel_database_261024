from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AddProperty, Room, Tenant, PaymentHistory, PaymentRemainder,ChangedPassword

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'mobile_number', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'mobile_number')
    ordering = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)


class AddPropertyAdmin(admin.ModelAdmin):
    list_display = ['hostelname', 'ownername', 'email', 'mobile', 'address']
    search_fields = ['hostelname', 'ownername', 'email', 'mobile']

admin.site.register(AddProperty, AddPropertyAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor_type', 'number_of_share', 'available_room_or_not', 'property']
    list_filter = ['property', 'floor_type']
    search_fields = ['room_number', 'property__hostelname']

admin.site.register(Room, RoomAdmin)


class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'adhar_number', 'room', 'property']
    list_filter = ['property', 'room']
    search_fields = ['name', 'email', 'mobile', 'adhar_number']

admin.site.register(Tenant, TenantAdmin)


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'amount_paid', 'date_paid', 'payment_method']
    list_filter = ['date_paid', 'payment_method']
    search_fields = ['tenant__name', 'reference_id']

admin.site.register(PaymentHistory, PaymentHistoryAdmin)


class PaymentRemainderAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'amount_paid', 'date_paid', 'payment_method']
    list_filter = ['date_paid', 'payment_method']
    search_fields = ['tenant__name', 'reference_id']

admin.site.register(PaymentRemainder, PaymentRemainderAdmin)

class ChangedPasswordAdmin(admin.ModelAdmin):
    list_display = ['user', 'forget_password_token', 'created_at']
    search_fields = ['user__username', 'forget_password_token']

admin.site.register(ChangedPassword, ChangedPasswordAdmin)
