from django.urls import path
from . import views

app_name = "medical"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("create-file/", views.createExp_view, name="create"),
    path('create-file/guardar-ficha', views.guarda_ficha_identificacion_view, name='guarda_ficha_identificacion'),
    path('create-file/antecedentes/<int:paciente_id>/', views.guarda_antecedentes_view, name='guarda_antecedentes'),
]
