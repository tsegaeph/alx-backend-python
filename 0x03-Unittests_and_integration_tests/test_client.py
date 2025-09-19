#!/usr/bin/env python3
"""Unittests and integration tests for GithubOrgClient"""
import unittest
from typing import Dict
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Test org returns correct value"""
        mock_get.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, {"name": org_name})
        mock_get.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "org",
                          new_callable=property) as mock_org:
            mock_org.return_value = {"repos_url": "http://test.com/repos"}
            self.assertEqual(client._public_repos_url, "http://test.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get):
        """Test public_repos method"""
        test_payload = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}}
        ]
        mock_get.return_value = test_payload
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=property) as mock_url:
            mock_url.return_value = "http://test.com/repos"
            repos = client.public_repos()
            self.assertEqual([r["name"] for r in test_payload], repos)
            mock_url.assert_called_once()
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                mock_resp = MagicMock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return MagicMock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos filtered by license"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
