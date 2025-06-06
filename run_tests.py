import pytest
import sys
import os

if __name__ == "__main__":
    # Set environment variable to indicate testing mode
    os.environ["FLASK_ENV"] = "testing"
    
    # Running all the unit tests
    print("Running the unit tests...")
    exit_code = pytest.main(["-v", "tests/unit/"])
    
    # To run selenium tests, uncomment the following lines:
    # print("Running the selenium tests...")
    # selenium_code = pytest.main(["-v", "tests/selenium/"])
    # exit_code = exit_code or selenium_code  # Use non-zero code if either test suite fails
    
    sys.exit(exit_code)
