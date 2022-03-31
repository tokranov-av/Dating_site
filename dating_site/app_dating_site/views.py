from django.contrib.auth import get_user_model
from rest_framework import permissions
from .filters import UsersFilter, CustomFilter
from .serializers import UserListSerializer
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import LikedUsers
from rest_framework.decorators import action
from .tasks import send_email_celery
from .paginations import UsersAPIListPagination


User = get_user_model()


class UsersAPIListViewSet(ReadOnlyModelViewSet):
    """
    Вывод списка пользователей с возможностью фильтрации имени, фамилии, полу,
     расстоянию от текущего авторизованного пользователя, а также установки
      отметки "Like".
    """
    serializer_class = UserListSerializer
    filterset_class = UsersFilter
    filter_backends = (CustomFilter,)
    permission_classes = (permissions.AllowAny,)
    pagination_class = UsersAPIListPagination

    def get_queryset(self):
        queryset = User.objects.filter(
            is_superuser=False, is_active=True, is_staff=False
        ).exclude(pk=self.request.user.id)
        return queryset

    @action(methods=['get'], detail=True, url_name='user_liked')
    def user_liked(self, request, *args, **kwargs):
        """Функция установки текущим пользователем отметки "Like" другому
         пользователю. В случае взаимной симпатии каждому из пользователей
          отравляется электронное письмо с email другого пользователя.
        """
        current_user = request.user
        liked_user = self.get_object()

        if isinstance(current_user, AnonymousUser):
            data = {'message': 'Пожалуйста, авторизуйтесь.'}
            return Response(data)

        data_current_user = LikedUsers.objects.filter(
            user_id=current_user.pk, liked_user_id=liked_user.pk
        ).first()

        if not data_current_user:
            LikedUsers.objects.create(
                user_id=current_user.pk, liked_user_id=liked_user.pk
            )

        data_liked_user = LikedUsers.objects.filter(
            user_id=liked_user.pk, liked_user_id=current_user.pk
        ).first()

        if data_liked_user:
            if (not data_current_user.send_email or
                    not data_liked_user.send_email):
                send_email_celery.delay(
                    current_user_pk=current_user.pk,
                    liked_user_pk=liked_user.pk
                )

        return Response(
            {
                'message':
                    f'Вы поставили Like пользователю {liked_user.first_name}.'
            }
        )
