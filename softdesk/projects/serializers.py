from rest_framework import serializers
from softdesk.accounts.models import SoftUser
from softdesk.projects.models import Project


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
