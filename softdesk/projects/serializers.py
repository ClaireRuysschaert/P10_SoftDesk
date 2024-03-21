from rest_framework import serializers
from softdesk.accounts.models import SoftUser
from softdesk.projects.models import Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=SoftUser.objects.all())

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "created_on",
            "updated_on",
            "author",
            "type",
            "contributors",
        ]
        # Allows to serialize author instance instead of its id
        depth = 1


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=SoftUser.objects.all())
    author_username = serializers.CharField(source="author.username", read_only=True)
    assign_to = serializers.PrimaryKeyRelatedField(
        queryset=SoftUser.objects.all()
    )
    assign_to_username = serializers.CharField(source="assign_to.username", read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    project_name = serializers.CharField(source="project.name", read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "description",
            "author",
            "author_username",
            "assign_to",
            "assign_to_username",
            "project",
            "project_name",
            "created_on",
            "updated_on",
            "status",
            "tag",
            "priority",
        ]

    def validate_assign_to(self, assign_to):
        issue: Issue = self.instance
        if issue: 
            project = issue.project
        else:
            project_id = self.context["request"].data["project"]
            project = Project.objects.get(pk=project_id)
        if project and assign_to not in project.contributors.all():
            raise serializers.ValidationError("Assignee must be a contributor of the project.")
        return assign_to
