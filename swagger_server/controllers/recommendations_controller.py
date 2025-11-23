import connexion
import six

from swagger_server.models.artist_recommendations import ArtistRecommendations  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.song_recommendations import SongRecommendations  # noqa: E501
from swagger_server import util
from swagger_server.dbconx.db_connection import dbConectar, dbDesconectar
from collections import Counter
import requests
import random
from swagger_server.controllers.authorization_controller import is_valid_token

TYA_SERVER = 'http://10.1.1.2:8001'
#todo recomendaciones... 
def check_auth(required_scopes=None):
    """
    Verifica autenticación defensiva (backup de Connexion).
    Devuelve (authorized, error_response) tuple.
    """
    token = connexion.request.cookies.get('oversound_auth')
    if not token or not is_valid_token(token):
        error = Error(code="401", message="Unauthorized: Missing or invalid token")
        return False, (error, 401)
    return True, None, token

def safe_get(url, timeout=5): #Method for json fetching
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

def get_artist_recs():  # noqa: E501
    """Get artist recommendations.

    Returns artist recommendations. # noqa: E501


    :rtype: List[ArtistRecommendations]
    """
    # Verificar autenticación defensiva
    authorized, error_response, token = check_auth(required_scopes=['read'])
    if not authorized:
        return error_response
    
    # if not connexion.request.is_json:
    #     return Error(code="400", message="Invalid JSON"), 400
    
    user = is_valid_token(token)
    user_id = user["userId"]

    try:
        connection = dbConectar()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT idArtista
        FROM HistorialArtistas
        WHERE idUsuario = %s
        GROUP BY idArtista;
        """, (user_id,))

        artists = cursor.fetchall()
        if not artists:
            return []  # or handle "no artists" case

        # Pick one random artist ID from the result list
        random_artist_id = random.choice(artists)[0] #Picks a random artist from the user's story


        data = safe_get(f"{TYA_SERVER}/artist/{random_artist_id}")
        if not data:
            return []
        
        song_ids=data.get("songs", []) #Gets their songs' ids
        random_songs = random.sample(song_ids, min(5, len(song_ids)))         

        genre_list = [] #make a list for the genres
        for song in random_songs:
            data = safe_get(f"{TYA_SERVER}/song/{song}")
            if not data:
                continue
            songs = data.get("genres", []) #get their genres
            if not songs:
                continue 
            genre_list.append(songs[0]) #put it in a list
     
        
        #We have a buncha genres
        canciones = []
        for g in genre_list:
            try:
                song_resp = requests.get(f"{TYA_SERVER}/song/filter", 
                                        params={"genres": g},
                                        timeout=5,
                                        headers={"Accept": "application/json"}
                                        )
                song_resp.raise_for_status()
                song_ids = song_resp.json() or []
            except Exception as e:
                print("Error calling genre filtering", e)
                continue 

            if not song_ids:
                continue

            sampled = random.sample(song_ids, min(3, len(song_ids)))
            canciones.extend(sampled)
        
        #Now we got a buncha song ids from each genre
        artist_list = set()
        for i in canciones:
            data = safe_get(f"{TYA_SERVER}/song/{i}")
            if not data:
                continue
            artist_list.add(data.get("artistId")) #we look for songs and then get the artists 's ids

        
        #now that we have the fucking artist id list, we get their info and pop it in the last list that we'll return
        recs = []
        for a in artist_list:
            data = safe_get(f"{TYA_SERVER}/artist/{a}")
            if not data:
                continue
            recs.append(
                ArtistRecommendations (
                    id = a,
                    name = data.get("name", "Jane Doe"),
                    image = data.get("imagen", None)
                )
            )

        return recs

    except Exception as e:
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500

    finally:
        if connection:
            dbDesconectar()


def get_song_recs():  # noqa: E501
    """Get song recommendations.

    Returns song recommendations. # noqa: E501


    :rtype: List[SongRecommendations]
    """
    # Verificar autenticación defensiva
    authorized, error_response, token = check_auth(required_scopes=['read'])
    if not authorized:
        return error_response
    
    # if not connexion.request.is_json:
    #     return Error(code="400", message="Invalid JSON"), 400
    
    user = is_valid_token(token)
    user_id = user["userId"]

    try:
        connection = dbConectar()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT idCancion
        FROM HistorialCanciones
        WHERE idUsuario = %s
        GROUP BY idCancion;
        """, (user_id,))

        db_songs = cursor.fetchall()
        if not db_songs:
            return [] 

        # db_songs is a list of tuples, e.g. [(12,), (55,), (102,)]
        random_songs = random.sample(db_songs, min(5, len(db_songs)))  # pick up to 3
        random_song_ids = [s[0] for s in random_songs]  # extract the IDs from tuples

        genre_list = set() #make a list for the genres, non-repeated
        for song in random_song_ids:
            data = safe_get(f"{TYA_SERVER}/song/{song}")
            if not data:
                continue
            songs = data.get("genres", []) #get their genres
            if not songs:
                continue 
            genre_list.add(songs[0]) #put it in a list
     
        
        #We have a buncha genres
        canciones = []
        for g in genre_list:
            try:
                song_resp = requests.get(f"{TYA_SERVER}/song/filter", 
                                        params={"genres": g},
                                        timeout=5,
                                        headers={"Accept": "application/json"}
                                        )
                song_resp.raise_for_status()
                song_ids = song_resp.json() or []
            except Exception as e:
                print("Error calling genre filtering", e)
                continue 

            if not song_ids:
                continue

            sampled = random.sample(song_ids, min(3, len(song_ids)))
            canciones.extend(sampled)

        
        #now that we have the fucking song id list, we get their info and pop it in the last list that we'll return
        recs = []
        for a in canciones:
            data = safe_get(f"{TYA_SERVER}/song/{a}")
            if not data:
                continue
            genres = data.get("genres", [])
            if not genres:
                continue  # or handle missing genres
            singular_genre = genres[0]
            recs.append(
                SongRecommendations (
                    id = a,
                    name = data.get("name", "Jane Doe"),
                    genre = singular_genre,
                    image = data.get("cover", None)
                )
            )

        return recs

    except Exception as e:
        if connection:
            connection.rollback()
        return Error(code="500", message="Internal server error"), 500

    finally:
        if connection:
            dbDesconectar()
