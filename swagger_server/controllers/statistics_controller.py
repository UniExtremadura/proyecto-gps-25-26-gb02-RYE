import connexion
import six

from swagger_server.models.artist_metrics import ArtistMetrics  # noqa: E501
from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_metrics import SongMetrics  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server import util
from swagger_server.dbconx.db_connection import dbConectar, dbDesconectar
from collections import Counter
import requests

TYA_SERVER = 'http://10.1.1.2:8081'

#Para estadisticas del artista
def get_artist_metrics(artist_id):  # noqa: E501
    """Get artist metrics by ID.

    Returns the artist&#x27;s all-time playblacks, number of songs, and current popularity placing. # noqa: E501

    :param artist_id: ID of artist.
    :type artist_id: int

    :rtype: ArtistMetrics
    """
    print(f"DEBUG: Starting get_artist_metrics with artist_id: {artist_id}")

    try:
        print("DEBUG: Connecting to database")
        connection = dbConectar()
        cursor = connection.cursor()

        #Playbacks
        print("DEBUG: Executing playbacks query")
        play_sql = """SELECT COALESCE(SUM(escuchas), 0)
                        FROM HistorialArtistas
                        WHERE idArtista = %s;"""

        cursor.execute(play_sql, 
                       (artist_id,))
        playbacks = cursor.fetchone()[0]
        print(f"DEBUG: Playbacks result: {playbacks}")



        print("DEBUG: Executing popularity ranking query")
        popu_sql = """
            SELECT idArtista, SUM(escuchas) AS total_playbacks
            FROM HistorialArtistas
            GROUP BY idArtista
            ORDER BY total_playbacks DESC;
        """
        cursor.execute(popu_sql)
        all_artists = cursor.fetchall()  #pilla idArtista, total_playbacks
        print(f"DEBUG: All artists fetched: {len(all_artists)} artists")


        popularity_rank = None
        for idx, (a_id, _) in enumerate(all_artists, start=1):
            if a_id == artist_id:
                popularity_rank = idx
                break
        print(f"DEBUG: Popularity rank for artist {artist_id}: {popularity_rank}")

        #Number of songs
        song_number = 0
        print(f"DEBUG: Fetching songs from API: {TYA_SERVER}/artist/{artist_id}")
        try:
            response = requests.get(f"{TYA_SERVER}/artist/{artist_id}")
            if response.status_code == 200: #if OK
                artist_data = response.json()
                songs = artist_data.get("owner_songs") or []
                song_number= len(songs)
                print(f"DEBUG: Songs fetched: {song_number}")
        except Exception as e:
            print(f"Error fetching songs from API: {e}")
            song_number = 0

        result = ArtistMetrics(
            id = artist_id,
            playbacks=playbacks,
            songs=song_number,
            popularity=popularity_rank
        )
        print(f"DEBUG: Returning ArtistMetrics: {result}")
        return result

    except Exception as e:
        print(f"Error getting artist metrics: {e}")
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500

    finally:
        if connection:
            print("DEBUG: Disconnecting from database")
            dbDesconectar(connection)


#Para estadisticas de la canción
def get_song_metrics(song_id):  # noqa: E501
    """Get song metrics by ID.

    Returns the song&#x27;s all-time playblacks, sales and downloads. # noqa: E501

    :param song_id: ID of chosen song.
    :type song_id: int

    :rtype: SongMetrics
    """
    print(f"DEBUG: Starting get_song_metrics with song_id: {song_id}")
    try:
        print("DEBUG: Connecting to database")
        connection = dbConectar()
        cursor = connection.cursor()

        #Playbacks
        print("DEBUG: Executing playbacks query")
        play_sql = """SELECT COALESCE(SUM(escuchas), 0)
                        FROM HistorialCanciones
                        WHERE idCancion = %s;"""

        cursor.execute(play_sql, 
                       (song_id,))
        playbacks = cursor.fetchone()[0]
        print(f"DEBUG: Playbacks result: {playbacks}")

        #Sales + downloads
        print("DEBUG: Executing sales query")
        sale_sql = """SELECT COUNT(*)
                        FROM HistorialCanciones
                        WHERE idCancion = %s;"""
        
        cursor.execute(sale_sql, 
                       (song_id,))
        sales= cursor.fetchone()[0]
        downloads = sales
        print(f"DEBUG: Sales and downloads: {sales}")

        result = SongMetrics(
            id = song_id,
            playbacks=playbacks,
            sales=sales,
            downloads=downloads
        )
        print(f"DEBUG: Returning SongMetrics: {result}")
        return result
    except Exception as e:
        print(f"Error getting song metrics: {e}")
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500

    finally:
        if connection:
            print("DEBUG: Disconnecting from database")
            dbDesconectar(connection)


#Para estadisticas del artista
def get_top10_artists():  # noqa: E501
    """Get the top 10 artists.

    Returns the most listened artists. # noqa: E501


    :rtype: List[ArtistRecommendations]
    """
    print("DEBUG: Starting get_top10_artists")
    try:
        print("DEBUG: Connecting to database")
        connection = dbConectar()
        cursor = connection.cursor()

        print("DEBUG: Executing top artists query")
        popu_sql = """
            SELECT idArtista, SUM(escuchas) AS total_playbacks
            FROM HistorialArtistas
            GROUP BY idArtista
            ORDER BY total_playbacks DESC
            LIMIT 10;
            """
        cursor.execute(popu_sql)
        top_artists = cursor.fetchall()  #pilla idArtista, total_playbacks
        print(f"DEBUG: Top artists fetched: {len(top_artists)} artists")

        top_10 = []

        for idx in top_artists:
            try:
                artist_id = idx[0]
                print(f"DEBUG: Fetching artist info from API: {TYA_SERVER}/artist/{artist_id}")
                response = requests.get(f"{TYA_SERVER}/artist/{artist_id}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    top_10.append(
                        ArtistRecommendations(
                            id=data.get("id", artist_id),
                            name=data.get("name", "Unknown Artist"),
                            image=data.get("image", None)
                        )
                    )
                    print(f"DEBUG: Added artist {artist_id} to top 10")
                else:
                    top_10.append(ArtistRecommendations(id=artist_id, name="Unknown", image=None))
                    print(f"DEBUG: Added unknown artist {artist_id} due to API error")
            except Exception as e:
                print(f"Error fetching artist info: {e}")
                top_10.append(ArtistRecommendations(id=artist_id, name="Unknown", image=None))
                print(f"DEBUG: Added unknown artist {artist_id} due to exception")
                
        print(f"DEBUG: Returning top 10 artists: {len(top_10)} items")
        return top_10
    except Exception as e:
        print(f"Error getting top 10 artists: {e}")
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500
    finally:
        if connection:
            print("DEBUG: Disconnecting from database")
            dbDesconectar(connection)

#Para estadisticas de la canción
def get_top10_songs():  # noqa: E501
    """Get the top 10 songs.

    Returns the most listened songs. # noqa: E501


    :rtype: List[SongRecommendations]
    """
    print("DEBUG: Starting get_top10_songs")
    try:
        print("DEBUG: Connecting to database")
        connection = dbConectar()
        cursor = connection.cursor()

        print("DEBUG: Executing top songs query")
        popu_sql = """
            SELECT idCancion, SUM(escuchas) AS total_playbacks
            FROM HistorialCanciones
            GROUP BY idCancion
            ORDER BY total_playbacks DESC
            LIMIT 10;
            """
        cursor.execute(popu_sql)
        top_songs = cursor.fetchall()  #pilla idCancion, total_playbacks
        print(f"DEBUG: Top songs fetched: {len(top_songs)} songs")

        top_10 = []

        for idx in top_songs:
            try:
                song_id = idx[0]
                print(f"DEBUG: Fetching song info from API: {TYA_SERVER}/song/{song_id}")
                response = requests.get(f"{TYA_SERVER}/song/{song_id}", timeout=5) 
                if response.status_code == 200:
                    data = response.json()
                    genre_ids=data.get("genres", [])
                    genre_id= genre_ids[0] if genre_ids else "Unknown" #no pienso cambiar el swagger otra vez, pillamos solo 1
                    top_10.append(
                        SongRecommendations(
                            id=data.get("songId", song_id),
                            name=data.get("title", "Unknown Artist"),
                            genre= genre_id,
                            image=data.get("cover", None)
                        )
                    )
                    print(f"DEBUG: Added song {song_id} to top 10")
                else:
                    top_10.append(SongRecommendations(id=song_id, name="Unknown", genre="Unknown", image=None))
                    print(f"DEBUG: Added unknown song {song_id} due to API error")
            except Exception as e:
                print(f"Error fetching song info: {e}")
                top_10.append(SongRecommendations(id=song_id, name="Unknown", genre="Unknown", image=None))
                print(f"DEBUG: Added unknown song {song_id} due to exception")

        print(f"DEBUG: Returning top 10 songs: {len(top_10)} items")
        return top_10
    except Exception as e:
        print(f"Error getting top 10 song: {e}")
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500
    finally:
        if connection:
            print("DEBUG: Disconnecting from database")
            dbDesconectar(connection)
