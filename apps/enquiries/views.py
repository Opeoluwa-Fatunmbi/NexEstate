from django.shortcuts import render
from adrf.views import APIView
from apps.common.responses import CustomResponse
from apps.enquiries.serializers import EnquirySerializer
from apps.enquiries.models import Enquiry
from apps.enquiries.emails import Util
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.throttling import UserRateThrottle
from apps.enquiries.pagination import EnquiryPagination
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class CreateEnquiryView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"
    pagination_class = EnquiryPagination
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Create an enquiry",
        request=EnquirySerializer,
        responses={201: EnquirySerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            enquiry = serializer.save()
            Util.send_enquiry(enquiry)
            return CustomResponse.success(
                message="Enquiry sent successfully",
                status_code=201,
                data=serializer.data,
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)


class GetEnquiriesView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"
    pagination_class = EnquiryPagination
    permission_classes = (IsAuthenticated,)

    @extend_schema(description="Get all enquiries", responses={200: EnquirySerializer})
    def get(self, request):
        try:
            enquiries = Enquiry.objects.all().values(
                "name", "email", "subject", "message"
            )
            serializer = self.serializer_class(enquiries, many=True)
            return CustomResponse.success(
                message="Enquiries fetched successfully",
                status_code=200,
                data=serializer.data,
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)


class GetEnquiryDetailView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Get a single enquiry", responses={200: EnquirySerializer}
    )
    def get(self, request, slug):
        try:
            enquiry = Enquiry.objects.get(slug=slug)
            serializer = self.serializer_class(enquiry)
            return CustomResponse.success(
                message="Enquiry fetched successfully",
                status_code=200,
                data=serializer.data,
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)


class GetAnsweredEnquiriesView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"

    @extend_schema(
        description="Get all answered enquiries", responses={200: EnquirySerializer}
    )
    def get(self, request):
        try:
            enquiries = Enquiry.objects.filter(is_answered=True)
            serializer = self.serializer_class(enquiries, many=True)
            return CustomResponse.success(
                message="Enquiries fetched successfully",
                status_code=200,
                data=serializer.data,
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)


class GetUnAnsweredEnquiriesView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"

    @extend_schema(
        description="Get all unanswered enquiries", responses={200: EnquirySerializer}
    )
    def get(self, request):
        try:
            enquiries = Enquiry.objects.filter(is_answered=False)
            serializer = self.serializer_class(enquiries, many=True)
            return CustomResponse.success(
                message="Enquiries fetched successfully",
                status_code=200,
                data=serializer.data,
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)


# DeleteEnquiryView [DELETE]:


class DeleteEnquiryView(APIView):
    serializer_class = EnquirySerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "enquiry"

    @extend_schema(description="Delete an enquiry", responses={204: None})
    def delete(self, request, slug):
        try:
            enquiry = Enquiry.objects.get(slug=slug)
            enquiry.delete()
            return CustomResponse.success(
                message="Enquiry deleted successfully", status_code=204
            )

        except Exception as e:
            return CustomResponse.error(message=str(e), status_code=500)
