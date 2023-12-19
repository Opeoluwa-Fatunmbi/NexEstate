# from rest_framework import serializers
# from apps.reports.models import PropertyValuationReport
# from apps.properties.models import Property
# from django.contrib.auth.models import User
# from apps.properties.serializers import PropertySerializer


# class PropertyValuationReportSerializer(serializers.Serializer):
#    user = serializers.PrimaryKeyRelatedField(
#        queryset=User.objects.all(), required=True
#    )
#    property = serializers.PrimaryKeyRelatedField(
#        queryset=Property.objects.all(), required=True
#    )
#    report = serializers.CharField(required=False)
#    generated = serializers.BooleanField(required=False)
#
#    def create(self, validated_data):
#        return PropertyValuationReport.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        instance.user = validated_data.get("user", instance.user)
#        instance.property = validated_data.get("property", instance.property)
#        instance.report = validated_data.get("report", instance.report)
#        instance.generated = validated_data.get("generated", instance.generated)
#        instance.save()
#        return instance
