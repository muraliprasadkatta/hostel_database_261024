from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AddProperty, Room, Tenant, ChangedPassword, History, Remainder, ManagementPin

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

class ManagementPinAdmin(admin.ModelAdmin):
    list_display = ['user', 'pin', 'created_at']
    search_fields = ['user__username', 'pin']

admin.site.register(ManagementPin, ManagementPinAdmin)

class AddPropertyAdmin(admin.ModelAdmin):
    list_display = ['hostelname', 'ownername', 'email', 'mobile', 'address']
    search_fields = ['hostelname', 'ownername', 'email', 'mobile']

admin.site.register(AddProperty, AddPropertyAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor_type', 'number_of_share', 'available_room_or_not', 'occupied_beds_display', 'property']
    list_filter = ['property', 'floor_type']
    search_fields = ['room_number', 'property__hostelname']

    def occupied_beds_display(self, obj):
        return obj.property.occupied_beds  # Accessing through the related AddProperty model

    occupied_beds_display.short_description = 'Occupied Beds'

admin.site.register(Room, RoomAdmin)

class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'property',]
    list_filter = ['property', 'room']
    search_fields = ['name', 'email', 'mobile', 'adhar_number']

admin.site.register(Tenant, TenantAdmin)

class ChangedPasswordAdmin(admin.ModelAdmin):
    list_display = ['user', 'forget_password_token', 'created_at']
    search_fields = ['user__username', 'forget_password_token']

admin.site.register(ChangedPassword, ChangedPasswordAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'amount_paid', 'date_paid']
    search_fields = ['tenant__name', 'tenant__room__room_number', 'tenant__property__hostelname']

admin.site.register(History, HistoryAdmin)

class RemainderAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'amount_paid', 'remaining_amount', 'payment_date', 'due_date', 'payment_type']
    search_fields = ['tenant__name', 'tenant__room__room_number', 'tenant__property__hostelname', 'payment_type', 'reference_number']
    list_filter = ['tenant__property', 'payment_type', 'payment_date', 'due_date']

admin.site.register(Remainder, RemainderAdmin)
