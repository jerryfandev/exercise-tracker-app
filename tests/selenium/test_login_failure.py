import unittest
import multiprocessing
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from backend import create_app
from backend.models import db

# Test config
PORT = 5001
URL = f"http://localhost:{PORT}/"

# Flask server for test run
def run_test_server():
    app = create_app()
    app.run(port=PORT)

class TestLoginFailure(unittest.TestCase):
    def setUp(self):
        # Set up Flask app and DB
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Start Flask server
        self.server_process = multiprocessing.Process(target=run_test_server)
        self.server_process.start()
        time.sleep(2)

        # Start browser
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(URL)

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()
        self.server_process.terminate()
        self.app_context.pop()

    def test_login_failure_shows_message(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Click "Log In" from homepage
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In"))).click()

        # Fill wrong credentials
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")

        # Submit login
        driver.find_element(By.ID, "login-button").click()

        # Wait for error message and assert
        error_elem = wait.until(EC.visibility_of_element_located((By.ID, "unsuccessful-login")))
        self.assertIn("Invalid username or password", error_elem.text)

if __name__ == "__main__":
    unittest.main()
