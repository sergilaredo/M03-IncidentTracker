from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connection  # Necessari per al SQL manual de l'apartat 4
from django.contrib.auth.decorators import login_required
from .models import Incident

# Apartats 2, 3, 9 i 10: Cercador (Vulnerable a XSS)
def cercador_vulnerable(request):
    q = request.GET.get('q', '')
    
    # Utilitzem l'ORM per evitar errors de sintaxi SQL quan injectis <script>,
    # però enviem la 'q' a la plantilla on el |safe provocarà el XSS.
    resultats = Incident.objects.filter(titol__icontains=q)
    
    return render(request, 'incidents/cerca.html', {'resultats': resultats, 'query': q})

# Apartat 4: Actualitzar correu (Vulnerable a SQLi UPDATE)
def actualitzar_correu(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        # Si l'usuari no està loguejat, posem 0 per evitar l'error "None" a SQL
        user_id = request.user.id if request.user.is_authenticated else 0
        
        # SQL Injection manual (Apartat 4)
        query = f"UPDATE auth_user SET email = '{email}' WHERE id = {user_id}"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            
        return HttpResponse(f"Perfil actualitzat correctament. Query executada: {query}")
    
    return render(request, 'incidents/perfil.html')

# Apartat 7 i 8: Detall (Protegit contra IDOR)
@login_required
def detall_incident_vulnerable(request, incident_id):
    # HARDENING (Apartat 8): Filtrem per ID i per l'usuari actual (request.user)
    # Si intentes veure un incident d'un altre, saltarà un 404.
    incident = get_object_or_404(Incident, id=incident_id, creador=request.user)
    
    return render(request, 'incidents/detall.html', {'incident': incident})