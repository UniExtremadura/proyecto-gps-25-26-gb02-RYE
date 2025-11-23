# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.history import History  # noqa: E501
from swagger_server.models.identifier import Identifier  # noqa: E501
from swagger_server.models.user_genres import UserGenres  # noqa: E501
from swagger_server.models.user_metrics import UserMetrics  # noqa: E501
from swagger_server.test import BaseTestCase


class TestHistoryController(BaseTestCase):
    """HistoryController integration test stubs"""

    def test_delete_artist_history(self):
        """Test case for delete_artist_history

        Deletes an artist from user's history.
        """
        body = Identifier()
        response = self.client.open(
            '/history/artists',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_song_history(self):
        """Test case for delete_song_history

        Deletes a song from user's history.
        """
        body = Identifier()
        response = self.client.open(
            '/history/songs',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_genre_count(self):
        """Test case for get_genre_count

        Get an user's genre count.
        """
        response = self.client.open(
            '/history/user-genres',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_metrics(self):
        """Test case for get_user_metrics

        Get an user's metrics.
        """
        response = self.client.open(
            '/history/user-metrics',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_new_song_history(self):
        """Test case for new_song_history

        Add a song to an user's song history.
        """
        body = History()
        response = self.client.open(
            '/history/songs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_artist_history(self):
        """Test case for post_artist_history

        Add an artist to an user's history.
        """
        body = History()
        response = self.client.open(
            '/history/artists',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
