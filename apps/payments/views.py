from adrf.views import APIView
from apps.common.responses import CustomResponse
from apps.properties.models import Property
from apps.properties.serializers import PropertySerializer
import stripe
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckOutSessionView(APIView):
    """
    Create a checkout session
    """

    serializer_class = PropertySerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a checkout session",
        responses={200: PropertySerializer},
    )
    def post(self, request, *args, **kwargs):
        """
        Create a checkout session
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            property = Property.objects.get(id=serializer.data["id"])
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": property.title,
                                "images": [property.cover_photo],
                            },
                            "unit_amount": property.final_property_price * 100,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=settings.SUCCESS_URL,
                cancel_url=settings.CANCEL_URL,
            )
            property.session_id = session.id
            property.save()
            return CustomResponse.success(
                data=serializer.data,
                status=200,
                message="Checkout session created successfully",
            )
        return CustomResponse.error(
            data=serializer.errors,
            status=400,
            message="Error creating checkout session",
        )


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    # For now, you only need to print out the webhook payload so you can see
    # the structure.
    print(payload)

    return HttpResponse(status=200)
