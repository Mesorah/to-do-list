from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from tdl import views

app_name = 'tdl'

item_api_router = SimpleRouter()
item_api_router.register(
    'api',
    views.ItemAPIViewSet,
    basename='item-api'
)

urlpatterns = [
    path('',  views.ListViewHome.as_view(), name='home'),
    path(
        'add_task_page',
        views.TaskCreateView.as_view(),
        name='add_task_page'
    ),
    path(
        'remove_task_page/<int:pk>/',
        views.TaskDeleteView.as_view(),
        name='remove_task_page'
    ),
    path(
        'update_task_page/<int:pk>/',
        views.TaskUpdateView.as_view(),
        name='update_task_page'
    ),
    path('item/search/', views.ListViewSearch.as_view(), name="search"),
    path(
        'item/<int:pk>/',
        views.DetailViewItemVisualization.as_view(),
        name="visualization"
    ),

    path(
        'api/user/<int:pk>/',
        views.item_api_user_detail,
        name='item_api_user_detail'
    ),

    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]


urlpatterns += item_api_router.urls
