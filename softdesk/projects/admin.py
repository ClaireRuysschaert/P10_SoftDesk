from django.contrib import admin

from softdesk.accounts.models import Contributor

from .models import Project

class ContributorInline(admin.TabularInline):
    model = Contributor

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', 'description', 'created_on', 'updated_on', 'author', 'type')
    search_fields = ('name', 'author', 'type')
    inlines = [ContributorInline]

class ContributorInline(admin.TabularInline):
    model = Contributor
