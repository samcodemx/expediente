from django.urls import path
from . import views

app_name = "medical"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("create-file/", views.createExp_view, name="create"),
    path('create-file/guardar-ficha/', views.guarda_ficha_identificacion_view, name='guarda_ficha_identificacion'),
    path('create-file/antecedentes/', views.guarda_antecedentes_view, name='guarda_antecedentes'),
    path('create-file/padecimiento/', views.guarda_padecimiento_view, name='guarda_padecimiento'),
    path('create-file/exploracion/', views.guarda_exploracion_view, name='guarda_exploracion'),
    #path('create-file/estudios/', views.guarda_estudios_view, name='guarda_estudios'),
    path('create-file/consulta/', views.guarda_consulta_view, name='guarda_consulta'),
]
