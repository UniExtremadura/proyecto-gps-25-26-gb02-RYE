import connexion
import six

from swagger_server.models.artist_metrics import ArtistMetrics  # noqa: E501
from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_metrics import SongMetrics  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server import util


def get_artist_metrics(artist_id):  # noqa: E501
    """Get artist metrics by ID.

    Returns the artist&#x27;s all-time playblacks, number of songs, and current popularity placing. # noqa: E501

    :param artist_id: ID of artist.
    :type artist_id: int

    :rtype: ArtistMetrics
    """
    return 'do some magic!'


def get_song_metrics(song_id):  # noqa: E501
    """Get song metrics by ID.

    Returns the song&#x27;s all-time playblacks, sales and downloads. # noqa: E501

    :param song_id: ID of chosen song.
    :type song_id: int

    :rtype: SongMetrics
    """
    return 'do some magic!'


def get_top10_artists():  # noqa: E501
    """Get the top 10 artists.

    Returns the most listened artists. # noqa: E501


    :rtype: List[ArtistRecommendations]
    """
    return 'do some magic!'


def get_top10_songs():  # noqa: E501
    """Get the top 10 songs.

    Returns the most listened songs. # noqa: E501


    :rtype: List[SongRecommendations]
    """
    return 'do some magic!'
