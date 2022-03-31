from rest_framework.pagination import PageNumberPagination


class UsersAPIListPagination(PageNumberPagination):
    """Класс пагинации списка пользователей."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
