from django.urls import path
from . import views

app_name = "medical"

# direccion: localhost/test
urlpatterns = [
    path("test", views.test, name="test"),
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("create-file", views.createExp_view, name="create"),
    path('create-file/', views.guarda_ficha_identificacion, name='guarda_ficha_identificacion'),
]
