from django.http import HttpRequest
from rest_framework import viewsets, permissions, serializers
from softdesk.projects.models import Issue, Project
from softdesk.projects.serializers import IssueSerializer, ProjectSerializer


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to edit it.
    """

    def has_permission(self, request: HttpRequest, view) -> bool:
        if view.action == ["update", "partial_update", "destroy"]:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        """
        Return True if the user is a contributor of the project.
        """
        if type(obj) == Issue:
            return request.user in obj.project.contributors.all()
        elif type(obj) == Project:
            return request.user in obj.contributors.all()



class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.

    Attributes:
        queryset (QuerySet): The queryset of projects.
        serializer_class (Serializer): The serializer class for projects.
        permission_classes (list): The list of permission classes for the viewset.
    """

    queryset = Project.objects.all().order_by("-created_on")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed or edited.

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (Serializer): The serializer class for issues.
        permission_classes (list): The list of permission classes for the viewset.
    """

    queryset = Issue.objects.all().order_by("-created_on")
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def perform_create(self, serializer: IssueSerializer):
        serializer.save(author=self.request.user)

    filterset_fields = ["project_id", "assign_to_id", "status", "priority"]
