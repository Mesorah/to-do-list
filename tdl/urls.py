from django.urls import path
from tdl import views


app_name = 'tdl'


urlpatterns = [
    path('',  views.home, name='home'),
    path('add_task_page', views.add_task_page, name='add_task_page'),
    path('add_task', views.add_task, name='add_task'),
    path('remove_task_page/<int:id>/', views.remove_task_page, name='remove_task_page'), # noqa E501
    path('update_task_page/<int:id>/', views.update_task_page, name='update_task_page'), # noqa E501
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('item/search/', views.search, name="search"),
    path('item/<int:id>', views.item_visualization, name="visualization"),
]
