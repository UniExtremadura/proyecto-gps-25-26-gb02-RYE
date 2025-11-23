# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRecommendationsController(BaseTestCase):
    """RecommendationsController integration test stubs"""

    def test_get_artist_recs(self):
        """Test case for get_artist_recs

        Get artist recommendations.
        """
        response = self.client.open(
            '/recommendations/artist',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_song_recs(self):
        """Test case for get_song_recs

        Get song recommendations.
        """
        response = self.client.open(
            '/recommendations/song',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
