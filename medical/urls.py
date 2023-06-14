from django.urls import path
from . import views

app_name = "medical"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("create-file/", views.createExp_view, name="create"),
    #path('create-file/guardar-ficha/', views.guarda_ficha_identificacion_view, name='guarda_ficha_identificacion'),
    path('create-file/antecedentes/', views.guarda_antecedentes_view, name='guarda_antecedentes'),
    path('create-file/padecimiento/', views.guarda_padecimiento_view, name='guarda_padecimiento'),


    # Ruta para ver el expediente
    path('view/<int:id_paciente>', views.ver_expediente_view, name='ver_expediente'),
    # Rutas nuevas para los formularios (create)
    path('create-file/ficha/', views.guarda_ficha_identificacion_view, name='guarda_ficha_identificacion'),
    path('create-file/antecedentes', views.createAntecedentes_view, name='crear_antecedentes'),
    path('create-file/padecimientos', views.createPadecimientos_view, name='crear_padecimientos'),
    path('create-file/exploracion', views.createExploracion_view, name='crear_exploracion'),
    path('create-file/consultas', views.createConsultas_view, name='crear_consultas'),
    # Rutas nuevas para los formularios (update)
    path('update-file/<int:id_paciente>/ficha/', views.update_ficha_identificacion_view, name='update_ficha_identificacion'),
    path('update-file/<int:id_paciente>/antecedentes/', views.updateAntecedentes_view, name='actualizar_antecedentes'),
    path('update-file/<int:id_paciente>/padecimientos/', views.updatePadecimientos_view, name='actualizar_padecimientos'),
    path('update-file/<int:id_paciente>/exploracion/', views.updateExploracion_view, name='actualizar_exploracion'),
    path('update-file/<int:id_paciente>/consultas/', views.updateConsultas_view, name='actualizar_consultas'),


]
