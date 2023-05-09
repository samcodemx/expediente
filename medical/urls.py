from django.urls import path
from . import views

app_name = "medical"

# direccion: localhost/test
urlpatterns = [
    path("test", views.test, name="test"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("", views.home_view, name="home"),
]
