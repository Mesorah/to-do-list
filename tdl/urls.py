from django.urls import path
from tdl import views


app_name = 'tdl'


urlpatterns = [
    path('',  views.ListViewHome.as_view(), name='home'),
    path('add_task', views.CreateTaskView.as_view(), name='add_task'),
    path('remove_task_page/<int:id>/',
         views.RemoveTaskView.as_view(),
         name='remove_task_page'
         ),
    path('update_task_page/<int:id>/',
         views.UpdateTaskView.as_view(),
         name='update_task_page'
         ),
    path('item/search/', views.ListViewSearch.as_view(), name="search"),
    path('item/<int:pk>/',
         views.DetailViewItemVisualization.as_view(),
         name="visualization"
         ),
]
