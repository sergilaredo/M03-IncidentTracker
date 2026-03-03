from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Selecció de navegador segons entorn
        browser = os.environ.get('SELENIUM_BROWSER', 'chrome').lower()
        
        if browser == 'firefox':
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            try:
                # Intentem utilitzar el driver ja present al sistema (GHA)
                cls.selenium = webdriver.Firefox(options=opts)
            except Exception:
                # Si falla, provem amb webdriver-manager (local/altres)
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                cls.selenium = webdriver.Firefox(service=service, options=opts)
        else:
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            opts = ChromeOptions()
            opts.add_argument("--headless")
            service = ChromeService(ChromeDriverManager().install())
            cls.selenium = webdriver.Chrome(service=service, options=opts)
            
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Assegurem que l'usuari de la fixture tingui la contrasenya que el test espera
        from django.contrib.auth.models import User
        u = User.objects.get(username='analista1')
        u.set_password('password123')
        u.save()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Anar a la pàgina de login
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        
        # 2. LOGIN (PUNT 2.2.3): Implementa el login amb 'analista1'
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("analista1")
        
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("password123") # Contrasenya que hem posat abans
        
        login_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']|//input[@type='submit']")
        login_button.click()
        
        # 3. Intentar forçar URL d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        
        # 4. ASSERT de Seguretat (Punt 2.2.3)
        # Si NO té permís, el títol serà diferent o ens demanarà login de nou
        admin_title = "Site administration | Django site admin"
        self.assertNotEqual(self.selenium.title, admin_title, "VULNERABILITAT: L'analista té accés a l'administració!")
