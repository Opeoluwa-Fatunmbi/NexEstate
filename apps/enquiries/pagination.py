from rest_framework.pagination import PageNumberPagination


class EnquiryPagination(PageNumberPagination):
    page_size = 4
