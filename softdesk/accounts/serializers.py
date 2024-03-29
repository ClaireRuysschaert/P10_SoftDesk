from rest_framework import serializers
from softdesk.accounts.models import SoftUser, Contributor

import datetime


class SoftUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftUser
        fields = [
            "id",
            "username",
            "email",
            "birthdate",
            "updated_on",
            "can_be_contacted",
            "can_be_shared",
        ]

    def validate_birthdate(self, value):
        today = datetime.date.today()
        age = (today - value) // datetime.timedelta(days=365.2425)
        if age < 15:
            raise serializers.ValidationError(
                "You must be at least 15 years old to create an account."
            )
        return value


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]
