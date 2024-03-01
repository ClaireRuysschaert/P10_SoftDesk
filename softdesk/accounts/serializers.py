from rest_framework import serializers
from softdesk.accounts.models import SoftUser

class SoftUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftUser
        fields = ["username", "email", "birthdate", "updated_on", "can_be_contacted", "can_be_shared"]
