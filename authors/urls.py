from django.urls import path
from authors import views


app_name = 'authors'


urlpatterns = [
    path('register/',
         views.AuthorRegisterView.as_view(),
         name='author_register'
         ),
    path('login/',
         views.AuthorLoginView.as_view(),
         name='author_login'
         ),
    path('logout/',
         views.AuthorLogoutView.as_view(),
         name='author_logout'
         )
]
