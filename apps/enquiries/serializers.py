from rest_framework import serializers
from apps.enquiries.models import Enquiry


class EnquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=30, default="+234703229589")
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new Enquiry instance, given the validated data.
        """
        return Enquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Enquiry instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.email = validated_data.get("email", instance.email)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.message = validated_data.get("message", instance.message)
        instance.save()
        return instance
