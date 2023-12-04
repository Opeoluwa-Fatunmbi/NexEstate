from rest_framework.pagination import PageNumberPagination


class AgentReviewPagination(PageNumberPagination):
    page_size = 4
