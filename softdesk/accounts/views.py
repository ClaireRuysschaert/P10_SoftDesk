from rest_framework import viewsets, permissions
from softdesk.accounts.models import Contributor, SoftUser
from softdesk.accounts.serializers import SoftUserSerializer, ContributorSerializer


class SoftUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SoftUser.objects.all().order_by("-date_joined")
    serializer_class = SoftUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contributors to be viewed or edited.
    """
    queryset = Contributor.objects.all().order_by("-date_joined").select_related("user", "project")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["project_id", "user_id"]
