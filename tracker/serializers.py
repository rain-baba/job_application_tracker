from rest_framework import serializers

from .models import Application, Company, InterviewRound


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = "__all__"


class InterviewRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewRound
        fields = "__all__"
