from django.http import HttpRequest
from rest_framework import viewsets, permissions, serializers
from softdesk.filters import CommentFilter
from softdesk.projects.models import Comment, Issue, Project
from softdesk.projects.serializers import CommentSerializer, IssueSerializer, ProjectSerializer


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to edit it.
    """

    def has_permission(self, request: HttpRequest, view) -> bool:
        """
        Return True if permission is granted to the request, else False
        """
        if view.action == 'create':
            if 'project' in request.data:
                project_id = request.data.get('project')
                project = Project.objects.get(pk=project_id)
                return request.user in project.contributors.all()
            elif 'issue' in request.data:
                issue_id = request.data.get('issue')
                issue = Issue.objects.get(pk=issue_id)
                return request.user in issue.project.contributors.all()
        return True


    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        """
        Return True if the user is a contributor of the project.
        """
        if not request.user.is_authenticated:
            return False
        if type(obj) == Comment:
            return request.user in obj.issue.project.contributors.all()
        elif type(obj) == Issue:
            return request.user in obj.project.contributors.all()
        elif type(obj) == Project:
            return request.user in obj.contributors.all()
        return False


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        """
        Return True if the user is the author of the object.
        """
        if not request.user.is_authenticated:
            return False
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.author == request.user
        return True


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
    permission_classes = [IsContributor, IsAuthor, permissions.IsAuthenticated]


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
    permission_classes = [IsContributor, IsAuthor, permissions.IsAuthenticated]
    filterset_fields = ["project_id", "assign_to_id", "status", "priority"]
    
    def perform_create(self, serializer: IssueSerializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.

    Attributes:
        queryset (QuerySet): The queryset of comments.
        serializer_class (Serializer): The serializer class for comments.
        permission_classes (list): The list of permission classes for the viewset.
    """
    queryset = Comment.objects.all().order_by("-created_on")
    serializer_class = CommentSerializer
    permission_classes = [IsContributor, IsAuthor, permissions.IsAuthenticated]
    filterset_class = CommentFilter

    def perform_create(self, serializer: CommentSerializer):
        serializer.save(author=self.request.user)
