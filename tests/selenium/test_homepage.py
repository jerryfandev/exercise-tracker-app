import unittest
import multiprocessing
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from backend import create_app

PORT = 5001
HOST = f"http://localhost:{PORT}/"

def run_flask_app():
    app = create_app("testing")
    app.run(port=PORT)

class TestHomepageLoad(unittest.TestCase):

    def setUp(self):
        # Set environment to testing
        os.environ["FLASK_ENV"] = "testing"

        # Start Flask app in separate process
        self.server = multiprocessing.Process(target=run_flask_app)
        self.server.start()
        time.sleep(2)  # Let the server boot

        # Start browser
        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(HOST)

    def tearDown(self):
        time.sleep(5)  # for visibility
        self.driver.quit()
        self.server.terminate()

    def test_homepage_loads(self):
        self.assertIn("Log In", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
