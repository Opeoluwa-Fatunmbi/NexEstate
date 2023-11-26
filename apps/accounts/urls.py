from django.urls import path
from apps.accounts.views import (
    LoginView,
    LogoutView,
    RegisterView,
    VerifyEmailView,
    ResendVerificationEmailView,
    SendPasswordResetOtpView,
    SetNewPasswordView,
    RefreshTokensView,
)

app_name = "apps.auth_module"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path(
        "send-password-reset-otp/",
        SendPasswordResetOtpView.as_view(),
        name="send-password-reset-otp",
    ),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set-new-password"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokensView.as_view(), name="refresh-tokens"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
