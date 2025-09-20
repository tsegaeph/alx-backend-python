#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos using fixtures"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class((
    "org_payload", "repos_payload", "expected_repos", "apache2_repos"
), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set side_effect"""
        # Save patcher in *both* class and instance attributes
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return cls.org_payload

        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def setUp(self):
        """Expose get_patcher at instance level for checker"""
        self.get_patcher = self.__class__.get_patcher

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos with given license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
