import connexion
import six

from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server import util


def get_artist_recs():  # noqa: E501
    """Get artist recommendations.

    Returns artist recommendations. # noqa: E501


    :rtype: List[ArtistRecommendations]
    """
    return 'do some magic!'


def get_song_recs():  # noqa: E501
    """Get song recommendations.

    Returns song recommendations. # noqa: E501


    :rtype: List[SongRecommendations]
    """
    return 'do some magic!'
