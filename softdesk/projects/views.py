from django.http import HttpRequest
from rest_framework import viewsets, permissions
from softdesk.projects.models import Project
from softdesk.projects.serializers import ProjectSerializer


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to edit it.
    """

    def has_permission(self, request:HttpRequest, view) -> bool:
        if view.action == ["update", "partial_update", "destroy"]:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request:HttpRequest, view, obj:Project) -> bool:
        """
        Return True if the user is a contributor of the project.
        """
        return request.user in obj.contributors.all()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    queryset = Project.objects.all().order_by("-created_on")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]


