from django.contrib import admin

from .models import SoftUser

@admin.register(SoftUser)
class SoftUserAdmin(admin.ModelAdmin):
    model = SoftUser
    list_display = ('username', 'email', 'birthdate', 'updated_on', 'can_be_contacted', 'can_be_shared')
    search_fields = ('username', 'email')
    list_filter = ('can_be_contacted', 'can_be_shared')
