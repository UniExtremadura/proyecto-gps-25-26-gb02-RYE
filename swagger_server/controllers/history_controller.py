import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.history import History  # noqa: E501
from swagger_server.models.identifier import Identifier  # noqa: E501
from swagger_server.models.user_genres import UserGenres  # noqa: E501
from swagger_server.models.user_metrics import UserMetrics  # noqa: E501
from swagger_server import util


def delete_artist_history(body=None):  # noqa: E501
    """Deletes an artist from user&#x27;s history.

    Delete an user&#x27;s artist history. # noqa: E501

    :param body: Some ID
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Identifier.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_song_history(body=None):  # noqa: E501
    """Deletes a song from user&#x27;s history.

    Delete an user&#x27;s song history. # noqa: E501

    :param body: Some ID
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Identifier.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_genre_count():  # noqa: E501
    """Get an user&#x27;s genre count.

    Returns the genre types that an user has listened to and the amount of songs per genre. # noqa: E501


    :rtype: List[UserGenres]
    """
    return 'do some magic!'


def get_user_metrics():  # noqa: E501
    """Get an user&#x27;s metrics.

    Returns an user&#x27;s top artist, top song and total listening time. # noqa: E501


    :rtype: UserMetrics
    """
    return 'do some magic!'


def new_song_history(body):  # noqa: E501
    """Add a song to an user&#x27;s song history.

    Add a song to an existing user&#x27;s song history. # noqa: E501

    :param body: Add a song to an user&#x27;s song history.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = History.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_artist_history(body):  # noqa: E501
    """Add an artist to an user&#x27;s history.

    Add an artist to an user&#x27;s history. # noqa: E501

    :param body: Adds an artist to an user&#x27;s history.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = History.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
