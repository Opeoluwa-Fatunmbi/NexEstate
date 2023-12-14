from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from .models import Property, PropertyViews, FavouriteProperty


class PropertySerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)
    cover_photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    photo1 = serializers.SerializerMethodField()
    photo2 = serializers.SerializerMethodField()
    photo3 = serializers.SerializerMethodField()
    photo4 = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_cover_photo(self, obj):
        return obj.cover_photo.url

    def get_photo1(self, obj):
        return obj.photo1.url

    def get_photo2(self, obj):
        return obj.photo2.url

    def get_photo3(self, obj):
        return obj.photo3.url

    def get_photo4(self, obj):
        return obj.photo4.url

    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url


class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Property
        exclude = ["updated_at", "pkid"]


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_at", "pkid"]


class FavouritePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProperty
        fields = "__all__"


class PropertyDescriptionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    country = CountryField(name_only=True)
    city = serializers.CharField(max_length=255)
    bedrooms = serializers.IntegerField()
    bathrooms = serializers.IntegerField()

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.save()
        return instance

    # def validate(self, data):
    #     if data["bedrooms"] > 10:
    #         raise serializers.ValidationError("Bedrooms cannot be more than 10")
    #     return data
    #
    # def validate_bedrooms(self, value):
    #     if value > 10:
    #         raise serializers.ValidationError("Bedrooms cannot be more than 10")
    #     return value
    #
    # def validate_bathrooms(self, value):
    #     if value > 10:
    #         raise serializers.ValidationError("Bathrooms cannot be more than 10")
    #     return value
