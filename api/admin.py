from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Post

# User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['verify_profiles']
    
    def verify_profiles(self, request, queryset):
        queryset.update(is_verified=True)
    verify_profiles.short_description = "Mark selected profiles as verified"

# Post Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'updated_at', 'is_active')
    list_filter = ('created_at', 'updated_at', 'is_active')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['activate_posts', 'deactivate_posts']
    
    def activate_posts(self, request, queryset):
        queryset.update(is_active=True)
    activate_posts.short_description = "Mark selected posts as active"
    
    def deactivate_posts(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_posts.short_description = "Mark selected posts as inactive"

# Customize User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
