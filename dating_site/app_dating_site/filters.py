from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, ExpressionWrapper, FloatField, Value, Func

User = get_user_model()


class UsersFilter(filters.FilterSet):
    """Фильтрация пользователя по полу, имени и фамилии."""
    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name')


class CustomFilter(DjangoFilterBackend):
    """
    Добавление фильтрации пользователей по расстоянию от текущего пользователя.
     Выводится список пользователей, расстояние до которых от текущего
      пользователя равно или меньше введенного значения.
    """
    def filter_queryset(self, request, queryset, view):
        """Функция фильтрации по дистанции относительно текущего пользователя.
         Дистанция рассчитывается по формуле Хаверсина."""
        distance = request.query_params.get('distance')

        if distance:
            try:
                current_user = request.user
                lat = float(current_user.latitude)
                lng = float(current_user.longitude)
                if all([lat, lng]):
                    distance = float(distance)
                    earth_radius = Value(6371.0, output_field=FloatField())
                    f1 = Func(F('latitude'), function='RADIANS')
                    latitude2 = Value(lat, output_field=FloatField())
                    f2 = Func(latitude2, function='RADIANS')

                    l1 = Func(F('longitude'), function='RADIANS')
                    longitude2 = Value(lng, output_field=FloatField())
                    l2 = Func(longitude2, function='RADIANS')

                    d_lat = f1 - f2
                    d_lng = l1 - l2

                    sin_lat = Func(d_lat / 2, function='SIN')
                    cos_lat1 = Func(f1, function='COS')
                    cos_lat2 = Func(f2, function='COS')
                    sin_lng = Func(d_lng / 2, function='SIN')

                    a = sin_lat ** 2 + cos_lat1 * cos_lat2 * sin_lng ** 2
                    c = 2 * Func(Func(a, function='SQRT'), function='ASIN')
                    d = earth_radius * c

                    queryset = User.objects.filter(
                        is_superuser=False, is_staff=False).exclude(
                        pk=current_user.pk).annotate(
                        radius=ExpressionWrapper(d, output_field=FloatField())
                    ).order_by('radius').filter(radius__lt=distance)
                    return queryset
            except ValueError:
                return {}
        queryset = super().filter_queryset(request, queryset, view)
        return queryset
