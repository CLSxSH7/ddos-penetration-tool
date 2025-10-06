"""
Unit tests for the DDoSClient class
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ddos_tool.core.ddos_client import DDoSClient


class TestDDoSClient(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = DDoSClient("http://example.com", 5)

    def test_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.target, "http://example.com")
        self.assertEqual(self.client.num_threads, 5)
        self.assertFalse(self.client.attack_running)
        self.assertEqual(self.client.attack_stats['requests_sent'], 0)
        self.assertEqual(self.client.attack_stats['success_count'], 0)
        self.assertEqual(self.client.attack_stats['error_count'], 0)

    @patch('ddos_tool.core.ddos_client.requests.get')
    def test_send_request_success(self, mock_get):
        """Test successful request"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.client.send_request()

        self.assertIsNone(result)

        self.client.attack_running = True
        result = self.client.send_request()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['code'], 200)
        self.assertEqual(self.client.attack_stats['requests_sent'], 1)
        self.assertEqual(self.client.attack_stats['success_count'], 1)

    @patch('ddos_tool.core.ddos_client.requests.get')
    def test_send_request_timeout(self, mock_get):
        """Test request timeout"""
        from requests.exceptions import Timeout
        mock_get.side_effect = Timeout()

        self.client.attack_running = True
        result = self.client.send_request()

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['type'], 'timeout')
        self.assertEqual(self.client.attack_stats['requests_sent'], 1)
        self.assertEqual(self.client.attack_stats['error_count'], 1)

    def test_format_target_with_protocol(self):
        """Test target formatting with existing protocol"""
        target = self.client._format_target("https://example.com")
        self.assertEqual(target, "https://example.com")

        target = self.client._format_target("http://test.org")
        self.assertEqual(target, "http://test.org")

    @patch('ddos_tool.core.ddos_client.requests.get')
    def test_format_target_without_protocol(self, mock_get):
        """Test target formatting without protocol"""
        # Test HTTPS success
        mock_get.return_value.status_code = 200
        target = self.client._format_target("example.com")
        self.assertEqual(target, "https://example.com")

        # Test HTTPS failure, should fallback to HTTP
        mock_get.side_effect = Exception("Connection failed")
        target = self.client._format_target("test.org")
        self.assertEqual(target, "http://test.org")


if __name__ == '__main__':
    unittest.main()
