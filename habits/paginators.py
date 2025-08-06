from rest_framework.pagination import PageNumberPagination


class HabitListPagination(PageNumberPagination):
    page_size = 5  # Количество объектов на странице
    page_size_query_param = "page_size"
    max_page_size = 5  # Максимально возможное количество объектов на странице