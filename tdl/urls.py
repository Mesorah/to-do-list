from django.urls import path

from tdl import views

app_name = 'tdl'


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
         'api/',
         views.ItemAPIv2ViewSet.as_view({
             'get': 'list',
             'post': 'create'
         }),
         name='item_api_list'
        ),
     path(
        'api/<int:pk>/',
        views.ItemAPIv2ViewSet.as_view({
             'get': 'retrieve',
             'patch': 'partial_update',
             'delete': 'destroy'
         }),
        name='item_api_detail'
     ),
     path(
         'api/user/<int:pk>/',
         views.item_api_user_detail,
         name='item_api_user_detail'
     ),
]
