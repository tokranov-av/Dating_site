from rest_framework.routers import DynamicRoute
from rest_framework import routers


class MyRouter(routers.SimpleRouter):
    """Маршрутизатор для API"""
    routes = [
        routers.Route(
            url=r'^{prefix}/list/$',
            mapping={'get': 'list'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/clients/{lookup}/match/$',
            name='{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
