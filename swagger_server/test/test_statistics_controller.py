# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.artist_metrics import ArtistMetrics  # noqa: E501
from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_metrics import SongMetrics  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStatisticsController(BaseTestCase):
    """StatisticsController integration test stubs"""

    def test_get_artist_metrics(self):
        """Test case for get_artist_metrics

        Get artist metrics by ID.
        """
        response = self.client.open(
            '/statistics/metrics/artist/{artistId}'.format(artist_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_song_metrics(self):
        """Test case for get_song_metrics

        Get song metrics by ID.
        """
        response = self.client.open(
            '/statistics/metrics/song/{songId}'.format(song_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_top10_artists(self):
        """Test case for get_top10_artists

        Get the top 10 artists.
        """
        response = self.client.open(
            '/statistics/top-10-artists',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_top10_songs(self):
        """Test case for get_top10_songs

        Get the top 10 songs.
        """
        response = self.client.open(
            '/statistics/top-10-songs',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
