from django.urls import path
from apps.payments.views import CreateCheckOutSessionView, stripe_webhook_view


app_name = "payments"

urlpatterns = [
    path("create-checkout-session/", CreateCheckOutSessionView.as_view()),
    path("stripe-webhook/", stripe_webhook_view),
]
