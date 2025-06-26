from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Destination, Contact, UserProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'created_at')}),
    )
    readonly_fields = ('created_at',)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'user')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language')
    search_fields = ('user__username', 'user__email', 'bio', 'interests')
    list_filter = ('preferred_language',) 