"""
Unit tests for input validation utilities
"""

import unittest
import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ddos_tool.ui.validators import validate_target


class TestValidators(unittest.TestCase):

    def test_validate_valid_url(self):
        """Test validation of valid URLs"""
        is_valid, message = validate_target("http://example.com")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid URL")

        is_valid, message = validate_target("https://test.org/path")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid URL")

    def test_validate_valid_ip(self):
        """Test validation of valid IP addresses"""
        is_valid, message = validate_target("192.168.1.1")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid IP address")

        is_valid, message = validate_target("10.0.0.1")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid IP address")

    def test_validate_invalid_target(self):
        """Test validation of invalid targets"""
        is_valid, message = validate_target("")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Target cannot be empty")

        is_valid, message = validate_target("invalid..target")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid target format")

    def test_validate_invalid_ip(self):
        """Test validation of invalid IP addresses"""
        is_valid, message = validate_target("999.999.999.999")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid target format")

        is_valid, message = validate_target("192.168.1")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid target format")


if __name__ == '__main__':
    unittest.main()
