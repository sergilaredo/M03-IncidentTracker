from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityTestCase(TestCase):
    def test_escalada_privilegis_sqli(self):
        # 1. Creem un usuari victima (que NO és superuser per defecte)
        user = User.objects.create_user(username='victima', password='password123')
        
        # 2. Loguegem l'usuari per poder accedir a /perfil/
        self.client.login(username='victima', password='password123')
        
        # 3. Simulem l'atac SQL Injection que has fet manualment
        # Intentem tancar la cometa de l'email i injectar el camp is_superuser
        payload = "test@email.com', is_superuser = '1"
        
        # Enviem el payload al formulari
        self.client.post(reverse('perfil'), {'email': payload})
        
        # 4. Refresquem l'objecte de l'usuari des de la DB temporal
        user.refresh_from_db()
        
        # 5. L'ASSERT: Verifiquem que l'usuari SEGUEIX SENSE SER superusuari.
        # Si el codi és vulnerable, user.is_superuser serà True i el test fallarà.
        self.assertFalse(
            user.is_superuser, 
            "VULNERABILITAT DETECTADA: Un usuari ha pogut escalar privilegis via SQLi al camp email!"
        )