import unittest
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from backend import create_app, db

def run_app():
    app = create_app()
    app.run(port=5001)

class BasicSeleniumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run_app)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)  # Keep browser open for 5 seconds

        cls.driver.quit()

    def test_homepage_loads(self):
        self.driver.get("http://localhost:5001/")
        self.assertIn("Log In", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()

