import unittest
import threading
import time

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

class TestProfileAccess(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.username = "testuser"
        self.password = "Password123"
        user = User(
            username=self.username,
            email="test@example.com",
            phone="0400000000",
            password_hash=generate_password_hash(self.password)
        )
        db.session.add(user)
        db.session.commit()

        # Start Flask server
        self.server_thread = threading.Thread(target=run_flask_server, args=(self.app,))
        self.server_thread.setDaemon(True)
        self.server_thread.start()
        time.sleep(2)

        # Start Selenium browser
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(HOST)

    def tearDown(self):
        time.sleep(3)
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_access_profile_page(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Login
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.username)
        driver.find_element(By.NAME, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        wait.until(EC.url_contains("dashboard"))

        # Go to profile
        driver.get(f"{HOST}/profile")
        wait.until(EC.presence_of_element_located((By.ID, "editBtn")))
        self.assertIn("profile", driver.current_url)

if __name__ == "__main__":
    unittest.main()
