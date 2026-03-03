from django.contrib import admin
from django.urls import path, include
from incidents.views import cercador_vulnerable, actualitzar_correu, detall_incident_vulnerable

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Rutes de login/logout
    path('buscar/', cercador_vulnerable, name='buscar'),
    path('perfil/', actualitzar_correu, name='perfil'),
    path('incident/<int:incident_id>/', detall_incident_vulnerable, name='detall_incident'),
]