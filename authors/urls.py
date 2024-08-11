from django.urls import path
from authors import views


app_name = 'authors'


urlpatterns = [
    path('register/',  views.author_register, name='author_register'),
    path('login/', views.author_login, name='author_login'),
    path('logout/', views.author_logout, name='author_logout')
]
