from apps.properties.models import Property
from adrf.views import APIView
from apps.common.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from apps.properties.serializers import PropertySerializer, PropertyCreateSerializer
from drf_spectacular.utils import extend_schema
from apps.properties.pagination import PropertyPagination
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PropertyListAPIView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PropertySerializer(many=True),
        description="List of all properties",
    )
    async def get(self, request):
        properties = await Property.objects.all().order_by("-created_at")

        serializer = PropertySerializer(properties, many=True)
        return CustomResponse(
            data=serializer.data, message="Properties retrieved successfully"
        )


class ListAgentsPropertiesView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination

    @extend_schema(
        responses=PropertySerializer(many=True),
        description="List of all properties",
    )
    async def get(self, request):
        properties = await Property.objects.filter(agent=request.user).order_by(
            "-created_at"
        )

        serializer = PropertySerializer(properties, many=True)
        return CustomResponse(
            data=serializer.data, message="Properties retrieved successfully"
        )


class PropertyDetailView(APIView):
    throttle_classes = [UserRateThrottle]
    pagination_class = PropertyPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PropertySerializer,
        description="Details of a property",
    )
    async def get(self, request, slug):
        property = await Property.objects.get(slug=slug)

        serializer = PropertySerializer(property)
        return CustomResponse(
            data=serializer.data, message="Property retrieved successfully"
        )


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


class CreatePropertyView(APIView):
    throttle_classes = [UserRateThrottle]
    paginagion_class = PropertyPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PropertySerializer,
        description="Details of a property",
    )
    async def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, message="Property created successfully"
            )
        else:
            return CustomResponse.error(
                data=serializer.errors, status_code=400, message="Invalid data"
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
        return CustomResponse(message="Property deleted successfully")


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
    serializer_class = PropertyCreateSerializer
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
    serializer_class = PropertyCreateSerializer
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
