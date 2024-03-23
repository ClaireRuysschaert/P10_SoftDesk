import django_filters
from softdesk.projects.models import Comment


class CommentFilter(django_filters.FilterSet):
    project_id = django_filters.NumberFilter(field_name='issue__project__id', label='Project ID')

    class Meta:
        model = Comment
        fields = ['author', 'issue', 'project_id']
