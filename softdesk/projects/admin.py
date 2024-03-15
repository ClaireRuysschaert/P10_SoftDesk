from django.contrib import admin

from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', 'description', 'created_on', 'updated_on', 'author', 'type')
    search_fields = ('name', 'author', 'type')
