from rest_framework import serializers
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    first_name = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    terms_agreement = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("first_name", instance.last_name)
        instance.terms_agreement = validated_data.get(
            "terms_agreement", instance.terms_agreement
        )
        instance.save()
        return instance


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8, error_messages={"min_length": _("{min_length} characters min.")}
    )
    terms_agreement = serializers.BooleanField()

    def validate(self, attrs):
        email = attrs["email"]
        terms_agreement = attrs["terms_agreement"]

        if len(email.split(" ")) > 1:
            raise serializers.ValidationError({"email": "No spacing allowed"})

        if terms_agreement != True:
            raise serializers.ValidationError(
                {"terms_agreement": "You must agree to terms and conditions"}
            )
        return attrs

    def create(self, validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        terms_agreement = validated_data["terms_agreement"]

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "This email is already registered"}
            )

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            terms_agreement=terms_agreement,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password = serializers.CharField(
        min_length=8, error_messages={"min_length": _("{min_length} characters min.")}
    )


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()


class FacebookLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class GoogleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
