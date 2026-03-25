from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mapa/', views.mapa, name='mapa'),

    path('cadastrar/restaurante/', views.cadastrar_restaurante, name='cadastrar_restaurante'),

    path('painel/comerciante/', views.painel_comerciante, name='painel_comerciante'),
    path('painel/secretaria/', views.painel_secretaria, name='painel_secretaria'),

    path('aprovar/<int:id>/', views.aprovar_restaurante, name='aprovar_restaurante'),
]