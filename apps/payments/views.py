from adrf.views import APIView
from apps.common.responses import CustomResponse
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
import stripe
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckOutSessionView(APIView):
    """
    Create a checkout session
    """

    serializer_class = PaymentSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = []

    @extend_schema(
        description="Create a checkout session",
        responses={200: PaymentSerializer},
    )
    def post(self, request, *args, **kwargs):
        """
        Create a checkout session
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        payment = Payment.objects.get(id=serializer.data["id"])
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": payment.product_name,
                            "images": [payment.product_image],
                        },
                        "unit_amount": payment.amount * 100,
                    },
                    "quantity": payment.quantity,
                }
            ],
            mode="payment",
            success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://example.com/cancel",
        )
        payment.session_id = session.id
        payment.save()
        return CustomResponse.success(
            data=serializer.data,
            status=200,
            message="Checkout session created successfully",
        )
