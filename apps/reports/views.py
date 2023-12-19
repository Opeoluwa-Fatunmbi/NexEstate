from adrf.views import APIView
from apps.common.responses import CustomResponse
from apps.properties.serializers import PropertySerializer
from apps.properties.models import Property
from apps.reports.emails import Util
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
import google.generativeai as genai
from apps.common.exceptions import RequestError
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)
from nexestate.settings.base import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


# Create your views here.


class PropertyValuationReportView(APIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    @extend_schema(
        description="Generate a property valuation report",
        responses={200: PropertySerializer},
        parameters=[
            OpenApiParameter(
                name="property_slug",
                description="Property slug",
                required=True,
                type=str,
                location="query",
            ),
        ],
    )
    async def patch(self, request, slug, *args, **kwargs):
        """
        Generate a property valuation report
        """

        # Use the patch method to generate a property valuation report using generative AI and save it to the property_valuation_report field in Property model

        # Get the property id from the request
        property_slug = request.GET.get("property_slug", None)
        property = await sync_to_async(Property.objects.get)(slug=property_slug)
        # Check if the property exists
        if not property:
            raise RequestError("Property does not exist")
        # Check if the property has been published
        if not property or not property.published_status:
            raise RequestError("Invalid property slug or property not published")

        # Generate a property valuation report using generative AI
        model = genai.GenerativeModel("gemini-pro")
        generated_report = model.generate_content(
            f"Generate a property valuation report for this property: {property.title}, {property.bedrooms} bedrooms, {property.bathrooms} bathrooms, located in {property.city}, {property.country}. I want it to account for {property.total_floors}, {property.tax}, {property.plot_area} square feet, {property.built_area} square feet, {property.parking}, {property.furnished}, {property.description}, {property.property_type},, {property.zip_code} {property.price} dollars. So we must have an introduction, a description of the property, a description of the neighborhood, scope of work, property description, market analysis, valuation approaches(Sales comparison approach, cost approach, income approach), conclusion."
        ).text

        # Save the generated report to the property_valuation_report field in Property model
        property.property_valuation_report = generated_report
        property.save()

        # Send the generated report to the user's email
        Util.send_property_valuation_report(
            property=property, user=request.user, report=generated_report
        )

        return CustomResponse.success(
            data=PropertySerializer(property).data,
            message="Property valuation report generated successfully",
        )
