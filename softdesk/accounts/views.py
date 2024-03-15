from rest_framework import viewsets, permissions
from softdesk.accounts.models import SoftUser
from softdesk.accounts.serializers import SoftUserSerializer


class SoftUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SoftUser.objects.all().order_by("-date_joined")
    serializer_class = SoftUserSerializer
    permission_classes = [permissions.IsAuthenticated]
