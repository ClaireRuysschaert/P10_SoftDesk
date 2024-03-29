from rest_framework import serializers
from softdesk.accounts.models import SoftUser
from softdesk.projects.models import Issue, Project, Comment


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


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=SoftUser.objects.all())
    assign_to = serializers.PrimaryKeyRelatedField(queryset=SoftUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "description",
            "author",
            "assign_to",
            "project",
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
            raise serializers.ValidationError(
                "Assignee must be a contributor of the project."
            )
        return assign_to


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=SoftUser.objects.all())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    project = serializers.PrimaryKeyRelatedField(source="issue.project", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "content",
            "author",
            "issue",
            "project",
            "created_on",
            "updated_on",
        ]
