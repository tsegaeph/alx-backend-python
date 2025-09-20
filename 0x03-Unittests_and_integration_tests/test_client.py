#!/usr/bin/env python3
"""Integration and unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value"""
        client = GithubOrgClient(org_name)
        mock_get_json.return_value = {"org": org_name}
        result = client.org
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        client = GithubOrgClient("google")
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        client = GithubOrgClient("google")
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "url"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide patcher for requests.get"""
        def get_json_side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return cls.org_payload

        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = lambda url, *a, **kw: Mock(json=lambda: get_json_side_effect(url))

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient(self.org_payload["repos_url"].split("/")[-2])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    def test_public_repos_without_license(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient(self.org_payload["repos_url"].split("/")[-2])
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )
