#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",), ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL"""
        payload = {"repos_url": "http://fake.url"}
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "org", new_callable=MagicMock) as mock_org:
            mock_org.return_value = payload
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("test")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=MagicMock
        ) as mock_url:
            mock_url.return_value = "http://fake.url"
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            self.assertEqual(client.public_repos("mit"), ["repo1"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


# Integration tests
from fixtures import TEST_PAYLOAD


@parameterized_class(TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher and mock requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            """Return correct fixture based on URL"""
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
        """Test public_repos returns expected repos list"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
