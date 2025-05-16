import unittest
import multiprocessing
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from backend import create_app
from backend.models import db

# Flask test server config
PORT = 5001
URL = f"http://localhost:{PORT}/"

# Top-level function to run Flask app in a separate process
def run_test_server():
    app = create_app()
    app.run(port=PORT)

class TestRegisterForm(unittest.TestCase):

    def setUp(self):
        # Set up Flask app and DB
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF manually
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Start Flask server in a separate process
        self.server_process = multiprocessing.Process(target=run_test_server)
        self.server_process.start()
        time.sleep(2)  # Give server time to start

        # Start Selenium browser
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Uncomment for headless
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(URL)

    def tearDown(self):
        time.sleep(5)  # for visibility

        self.driver.quit()
        self.server_process.terminate()
        self.app_context.pop()

    def test_successful_registration(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Click the "Register" button on homepage to open register page
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register"))).click()

        # Generate unique values
        uid = str(random.randint(1000, 9999))
        username = f"testuser{uid}"
        email = f"test{uid}@example.com"
        phone = f"040000{uid}"
        password = "Password123"

        # Wait for form to appear
        wait.until(EC.presence_of_element_located((By.NAME, "username")))

        # Fill form fields
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone").send_keys(phone)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)

        # Submit form
        driver.find_element(By.ID, "register-button").click()


        # Assert user is redirected to login or dashboard
        wait.until(EC.url_contains("login"))
        self.assertIn("login", driver.current_url.lower())
 

if __name__ == "__main__":
    unittest.main()
