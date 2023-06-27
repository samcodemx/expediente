from django.urls import path
from . import views

app_name = "medical"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("create-file/", views.createExp_view, name="create"),
    path('create-file/antecedentes/', views.renderiza_antecedentes_view, name='render_antecedentes'),
    path('create-file/padecimiento/', views.renderiza_padecimiento_view, name='render_padecimiento'),
    path('create-file/exploracion/', views.renderiza_exploracion_view, name='render_exploracion'),
    path('create-file/consultas/', views.renderiza_consulta_view, name='render_consultas'),
    path('help/', views.renderiza_ayuda_view, name='help'),

    # Ruta para ver el expediente
    path('view/<int:id_paciente>/', views.ver_expediente_view, name='ver_expediente'),
    path('delete/<int:id_paciente>/', views.elimina_paciente_view, name='elimina_paciente'),

    # Rutas nuevas para los formularios (create)
    path('create-file/ficha/', views.guarda_ficha_identificacion_view, name='guarda_ficha_identificacion'),
    path('create-file/antecedentes/<int:id_paciente>/', views.guarda_antecedentes_view, name='guarda_antecedentes'),
    path('create-file/padecimiento/<int:id_paciente>/', views.guarda_padecimiento_view, name='guarda_padecimiento'),
    path('create-file/exploracion/<int:id_paciente>/', views.guarda_exploracion_view, name='guarda_exploracion'),
    path('create-file/consultas/<int:id_paciente>/', views.guarda_consulta_view, name='guarda_consultas'),

    # Rutas nuevas para los formularios (update)
    path('update-file/<int:id_paciente>/ficha/', views.update_ficha_identificacion_view, name='update_ficha_identificacion'),
    path('update-file/<int:id_paciente>/antecedentes/', views.update_antecedentes_view, name='update_antecedentes'),
    path('update-file/<int:id_paciente>/padecimiento/', views.update_padecimiento_view, name='update_padecimiento'),
    path('update-file/<int:id_paciente>/exploracion/', views.update_exploracion_view, name='update_exploracion'),
    path('update-file/<int:id_paciente>/consultas/', views.update_consultas_view, name='update_consultas'),

    # Consulta desde el view
    path('add/consulta/', views.add_consulta_view, name='agregar_consulta'),
]
