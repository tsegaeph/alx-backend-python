#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected dictionary"""
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test _public_repos_url property returns the correct URL"""
        payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        client = GithubOrgClient("test-org")

        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url

        self.assertEqual(result, payload["repos_url"])
