from adrf.views import APIView
from apps.common.responses import CustomResponse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.throttling import UserRateThrottle
from apps.common.exceptions import RequestError
from apps.common.responses import CustomResponse
from apps.accounts.models import User, Otp, Jwt
from apps.accounts.serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    LoginSerializer,
    ResendOtpSerializer,
    RefreshSerializer,
    SetNewPasswordSerializer,
)
from apps.accounts.emails import Util

from apps.accounts.auth import Authentication
from apps.common.exceptions import RequestError
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.common.utils import IsAuthenticatedCustom
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import GenericAPIView
from .serializers import (
    GoogleSocialAuthSerializer,
    TwitterAuthSerializer,
    FacebookSocialAuthSerializer,
)


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Register a new user",
        description="This endpoint registers new users into our application",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check for existing user
        existing_user = await User.objects.get_or_none(email=data["email"])
        if existing_user:
            raise RequestError(
                err_msg="Invalid Entry",
                status_code=422,
                data={"email": "Email already registered!"},
            )

        # Create user
        user = await User.objects.create_user(**data)

        # Send verification email
        await Util.send_activation_otp(user)

        return CustomResponse.success(
            message="Registration successful",
            data={"email": data["email"]},
            status_code=201,
        )


class LoginView(APIView):
    serializer_class = LoginSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = (IsAuthenticatedCustom,)

    @extend_schema(
        summary="Login a user",
        description="This endpoint generates new access and refresh tokens for authentication",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data["email"]
        password = data["password"]

        user = await User.objects.get_or_none(email=email)
        if not user or not user.check_password(password):
            raise RequestError(err_msg="Invalid credentials", status_code=401)

        if not user.is_email_verified:
            raise RequestError(err_msg="Verify your email first", status_code=401)
        await Jwt.objects.filter(user_id=user.id).adelete()

        # Create tokens and store in jwt model
        access = Authentication.create_access_token({"user_id": str(user.id)})
        refresh = Authentication.create_refresh_token()
        await Jwt.objects.acreate(user_id=user.id, access=access, refresh=refresh)

        return CustomResponse.success(
            message="Login successful",
            data={"access": access, "refresh": refresh},
            status_code=201,
        )


class LogoutView(APIView):
    serializer_class = None
    permission_classes = (IsAuthenticatedCustom,)

    @extend_schema(
        summary="Logout a user",
        description="This endpoint logs a user out from our application",
    )
    async def get(self, request):
        await Jwt.objects.filter(user_id=request.user.id).adelete()
        return CustomResponse.success(message="Logout successful")


class VerifyEmailView(APIView):
    serializer_class = VerifyOtpSerializer

    @extend_schema(
        summary="Verify a user's email",
        description="This endpoint verifies a user's email",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]

        user = await User.objects.get_or_none(email=email)

        if not user:
            raise RequestError(err_msg="Incorrect Email", status_code=404)

        if user.is_email_verified:
            return CustomResponse.success(message="Email already verified")

        otp = await Otp.objects.get_or_none(user=user)
        if not otp or otp.code != otp_code:
            raise RequestError(err_msg="Incorrect Otp", status_code=404)
        if otp.check_expiration():
            raise RequestError(err_msg="Expired Otp")

        user.is_email_verified = True
        await user.asave()
        await otp.adelete()

        # Send welcome email
        Util.welcome_email(user)
        return CustomResponse.success(
            message="Account verification successful", status_code=200
        )


class ResendVerificationEmailView(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
        summary="Resend Verification Email",
        description="This endpoint resends new otp to the user's email",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = await User.objects.get_or_none(email=email)
        if not user:
            raise RequestError(err_msg="Incorrect Email", status_code=404)
        if user.is_email_verified:
            return CustomResponse.success(message="Email already verified")

        # Send verification email
        await Util.send_activation_otp(user)
        return CustomResponse.success(
            message="Verification email sent", status_code=200
        )


class SendPasswordResetOtpView(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
        summary="Send Password Reset Otp",
        description="This endpoint sends new password reset otp to the user's email",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = await User.objects.get_or_none(email=email)
        if not user:
            raise RequestError(err_msg="Incorrect Email", status_code=404)

        # Send password reset email
        await Util.send_password_change_otp(user)
        return CustomResponse.success(message="Password otp sent")


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    @extend_schema(
        summary="Set New Password",
        description="This endpoint verifies the password reset otp",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data["email"]
        code = data["otp"]
        password = data["password"]

        user = await User.objects.get_or_none(email=email)
        if not user:
            raise RequestError(err_msg="Incorrect Email", status_code=404)

        otp = await Otp.objects.get_or_none(user=user)
        if not otp or otp.code != code:
            raise RequestError(err_msg="Incorrect Otp", status_code=404)

        if otp.check_expiration():
            raise RequestError(err_msg="Expired Otp")

        user.set_password(password)
        await user.asave()

        # Send password reset success email
        Util.password_reset_confirmation(user)
        return CustomResponse.success(message="Password reset successful")


class RefreshTokensView(APIView):
    serializer_class = RefreshSerializer
    permission_classes = (IsAuthenticatedCustom,)

    @extend_schema(
        summary="Refresh tokens",
        description="This endpoint refresh tokens by generating new access and refresh tokens for a user",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = data["refresh"]
        jwt = await Jwt.objects.get_or_none(refresh=token)

        if not jwt:
            raise RequestError(err_msg="Refresh token does not exist", status_code=404)
        if not Authentication.decode_jwt(token):
            raise RequestError(
                err_msg="Refresh token is invalid or expired", status_code=401
            )

        access = Authentication.create_access_token({"user_id": str(jwt.user_id)})
        refresh = Authentication.create_refresh_token()

        jwt.access = access
        jwt.refresh = refresh
        await jwt.asave()

        return CustomResponse.success(
            message="Tokens refresh successful",
            data={"access": access, "refresh": refresh},
            status_code=201,
        )


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return CustomResponse(data, status=200)


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an access token as from facebook to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return CustomResponse(data, status=200)


class TwitterSocialAuthView(GenericAPIView):
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return CustomResponse(serializer.validated_data, status=200)
