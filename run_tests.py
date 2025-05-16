import unittest
import sys
import os

if __name__ == "__main__":
    # Set environment variable to indicate test mode
    os.environ["FLASK_ENV"] = "testing"
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests/unit', pattern='test_*.py')
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero code if any tests failed
    sys.exit(not result.wasSuccessful())
