from django.urls import path
from . import views

app_name = 'medical'

#direccion: localhost/test
urlpatterns = [
    path('test', views.index, name='index'),

]