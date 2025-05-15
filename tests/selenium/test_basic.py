import unittest
import multiprocessing
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from backend import create_app, db
from backend.models import User

# Flask setup
PORT = 5001
localHost = f"http://localhost:{PORT}/"
testApp = create_app()

def run_flask_server():
    testApp.run(port=PORT)

class SeleniumTests(unittest.TestCase):

    def setUp(self):
        self.app_context = testApp.app_context()
        self.app_context.push()

        db.create_all()
        self.add_test_data()

        # ✅ Launch Flask using multiprocessing with a top-level function
        self.server_process = multiprocessing.Process(target=run_flask_server)
        self.server_process.start()
        time.sleep(1)  # wait for server to boot

        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        time.sleep(5)  # for visibility
        self.driver.quit()
        self.server_process.terminate()
        self.app_context.pop()

    def add_test_data(self):
        # No test data yet, placeholder for login test
        pass

    def test_homepage_has_login_button(self):
        self.assertIn("Log In", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
