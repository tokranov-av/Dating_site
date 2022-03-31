from django.urls import path, include
from .views import UsersAPIListViewSet
from .routers import MyRouter


router = MyRouter()
router.register('api', UsersAPIListViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
