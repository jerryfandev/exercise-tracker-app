import unittest
import threading
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from backend import create_app, db
from backend.models import User
from werkzeug.security import generate_password_hash

PORT = 5001
HOST = f"http://localhost:{PORT}"

def run_flask_server(app):
    app.run(port=PORT)

class TestLoginForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # ✅ Add a test user
        self.test_username = "testuser"
        self.test_password = "Password123"
        test_user = User(
            username=self.test_username,
            email="test@example.com",
            phone="0400000000",
            password_hash=generate_password_hash(self.test_password)
        )
        db.session.add(test_user)
        db.session.commit()

        # ✅ Start Flask server in a background thread
        self.server_thread = threading.Thread(target=run_flask_server, args=(self.app,))
        self.server_thread.setDaemon(True)
        self.server_thread.start()
        time.sleep(1)  # give server time to boot

        # ✅ Launch Selenium browser
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(HOST)

    def tearDown(self):
        time.sleep(5)  # for visibility
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_successful_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # ✅ Go to login page
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In"))).click()

        # ✅ Fill form
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(self.test_username)
        driver.find_element(By.NAME, "password").send_keys(self.test_password)

        # ✅ Submit
        driver.find_element(By.ID, "login-button").click()

        # ✅ Wait for redirect to dashboard
        wait.until(EC.url_contains("dashboard"))
        self.assertIn("dashboard", driver.current_url)

if __name__ == "__main__":
    unittest.main()
