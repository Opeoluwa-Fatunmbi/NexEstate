from django.shortcuts import get_object_or_404
from apps.properties.models import Property, PropertyViews, FavouriteProperty
from adrf.views import APIView
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from apps.common.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import ListAPIView
from apps.properties.serializers import (
    PropertySerializer,
    PropertyCreateSerializer,
    FavouritePropertySerializer,
    # PropertyDescriptionSerializer,
)
from drf_spectacular.utils import extend_schema
from apps.properties.pagination import PropertyPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import django_filters
import google.generativeai as genai
from asgiref.sync import sync_to_async


logger = logging.getLogger(__name__)
from nexestate.settings.base import GOOGLE_API_KEY


genai.configure(api_key=GOOGLE_API_KEY)


# for m in genai.list_models():
#    if "generateContent" in m.supported_generation_methods:
#        print(m.name)
# model = genai.GenerativeModel("gemini-pro")
# response = model.generate_content("What is the meaning of life?")
# print(response.text)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )

    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "price"]


# Create your views here.
class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]


class ListAgentsPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by("-created_at")
        return queryset


# class PropertyDetailView(APIView):
#    throttle_classes = [UserRateThrottle]
#    pagination_class = PropertyPagination
#    permission_classes = [IsAuthenticated]
#
#    @extend_schema(
#        responses=PropertySerializer,
#        description="Details of a property",
#    )
#    async def get(self, request, slug):
#        property = await Property.objects.get(slug=slug)
#
#        serializer = PropertySerializer(property)
#        return CustomResponse.success(
#            data=serializer.data,
#            message="Property retrieved successfully",
#            status_code=200,
#        )
#


class UpdatePropertyView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination

    @extend_schema(
        responses=PropertySerializer,
        description="Update details of a property",
    )
    async def put(self, request, slug):
        property = await Property.objects.get(slug=slug)

        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, message="Property updated successfully"
            )
        else:
            return CustomResponse.error(
                data=serializer.errors, status_code=400, message="Invalid data"
            )


# class UpdatePropertyDescriptionView(APIView):
#    serializer_class = PropertyDescriptionSerializer
#    throttle_classes = [UserRateThrottle]
#    paginagion_class = PropertyPagination
#
#    @extend_schema(
#        responses=PropertySerializer,
#        description="Update details of a property",
#    )
#    async def put(self, request, slug):
#        property = await Property.objects.get(slug=slug)
#
#        # Update property details based on request data
#
#        serializer = PropertyDescriptionSerializer(
#            property, data=request.data, partial=True
#        )
#        if serializer.is_valid():
#            # Generate description using Gemini Pro
#            model = genai.GenerativeModel("gemini-pro")
#            generated_description = model.generate_content(
#                f"Describe this property: {serializer.data['title']}, {serializer.data['bedrooms']} bedrooms, {serializer.data['bathrooms']} bathrooms, located in {serializer.data['city']}, {serializer.data['country']}."
#            ).text
#
#            # Update property description with generated content
#            property.description = generated_description
#            serializer.save()
#
#            return CustomResponse.success(
#                data=serializer.data,
#                status_code=200,
#                message="Property updated successfully",
#            )
#        else:
#            return CustomResponse.error(
#                data=serializer.errors, status_code=400, message="Invalid data"
#            )
#


class CreatePropertyView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination
    serializer_class = PropertyCreateSerializer

    @extend_schema(
        responses=PropertySerializer,
        description="Create a new property",
    )
    async def post(self, request):
        serializer = PropertyCreateSerializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)(user=request.user)
            return CustomResponse.success(
                data=serializer.data,
                message="Property created successfully",
                status_code=201,
            )
        else:
            return CustomResponse.error(
                data=serializer.errors,
                status_code=400,
                message="Invalid data",
                status=400,
            )


class DeletePropertyView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination

    @extend_schema(
        responses=PropertySerializer,
        description="Details of a property",
    )
    async def delete(self, request, slug):
        property = await Property.objects.get(slug=slug)

        property.delete()
        return CustomResponse.success(message="Property deleted successfully")


class UploadPropertyImageView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination

    @extend_schema(
        responses=PropertySerializer,
        description="Details of a property",
    )
    async def post(self, request, slug):
        property = await Property.objects.get(slug=slug)

        if request.FILES:
            property.photo1 = request.FILES["photo1"]
            property.photo2 = request.FILES["photo2"]
            property.photo3 = request.FILES["photo3"]
            property.photo4 = request.FILES["photo4"]
            property.save()
            return CustomResponse.success(
                message="Property images uploaded successfully"
            )
        else:
            return CustomResponse.error(
                data={}, status_code=400, message="Invalid data"
            )


class PropertySearchAPIView(APIView):
    throttle_classes = [UserRateThrottle]
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PropertySerializer(many=True),
        description="List of all properties",
    )
    def post(self, request):
        queryset = Property.objects.filter(published_status=True)
        data = self.request.data

        advert_type = data["advert_type"]
        queryset = queryset.filter(advert_type__iexact=advert_type)

        property_type = data["property_type"]
        queryset = queryset.filter(property_type__iexact=property_type)

        price = data["price"]
        if price == "$0+":
            price = 0
        elif price == "$50,000+":
            price = 50000
        elif price == "$100,000+":
            price = 100000
        elif price == "$200,000+":
            price = 200000
        elif price == "$400,000+":
            price = 400000
        elif price == "$600,000+":
            price = 600000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price)

        bedrooms = data["bedrooms"]
        if bedrooms == "0+":
            bedrooms = 0
        elif bedrooms == "1+":
            bedrooms = 1
        elif bedrooms == "2+":
            bedrooms = 2
        elif bedrooms == "3+":
            bedrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4
        elif bedrooms == "5+":
            bedrooms = 5

        queryset = queryset.filter(bedrooms__gte=bedrooms)

        bathrooms = data["bathrooms"]
        if bathrooms == "0+":
            bathrooms = 0.0
        elif bathrooms == "1+":
            bathrooms = 1.0
        elif bathrooms == "2+":
            bathrooms = 2.0
        elif bathrooms == "3+":
            bathrooms = 3.0
        elif bathrooms == "4+":
            bathrooms = 4.0

        queryset = queryset.filter(bathrooms__gte=bathrooms)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)

        return CustomResponse.success(serializer.data)


class PropertyTaxAPIView(APIView):
    throttle_classes = [UserRateThrottle]
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PropertySerializer(many=True),
        description="Get the tax of a property",
    )
    def get(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)

            tax = property.price * property.tax
            return CustomResponse.success(tax)
        except:
            return CustomResponse.error(
                data={}, status_code=400, message="Invalid data"
            )


class AddToFavouritesView(APIView):
    """
    API view to add a property to user's favorites.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses=FavouritePropertySerializer,
        description="Add property to favorites",
    )
    async def post(self, request, slug):
        property = await get_object_or_404(Property, slug=slug)

        # Create a new FavouriteProperty instance
        favourite_property_data = {"user": request.user.id, "property": property.id}
        serializer = FavouritePropertySerializer(data=favourite_property_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Property added to favorites",
            )

        return CustomResponse.error(data=serializer.errors, message="Server error")


class DeletePropertyFromFavouritesView(APIView):
    """
    API view to remove a property from user's favorites.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses=status.HTTP_204_NO_CONTENT,
        description="Remove property from favorites",
    )
    async def post(self, request, slug):
        property = await get_object_or_404(Property, slug=slug)

        try:
            FavouriteProperty.objects.filter(
                user=request.user, property=property
            ).delete()
            return CustomResponse.success(
                message="Property removed from favorites",
            )

        except Exception:
            return CustomResponse.error(message="Server Error")


class ListFavoritePropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by("-created_at")
        return queryset
