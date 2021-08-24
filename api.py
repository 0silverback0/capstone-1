import requests
from config import API_SECRET_KEY

BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

def get_artist_id(artist):
    """ returns artist id from api """

    res = requests.get(f'{BASE_URL}artist.search',
    params={'q_artist': artist, 'page_size': 1, 'apikey': API_SECRET_KEY})

    data = res.json()
    artist_id = data['message']['body']['artist_list'][0]['artist']['artist_id']

    return artist_id

def get_artist_albums(artist_id):
    """ returns a list of artist albums from api """
    ###fix duplicates that are spelled different and no data
    res = requests.get(f'{BASE_URL}artist.albums.get', params={'artist_id': artist_id, 'apikey': API_SECRET_KEY})
    data = res.json()
    album_data = data['message']['body']['album_list']
    albums = []
    get_album_list = [albums.append( album['album']['album_name']) for album in album_data if album['album']['album_name'] not in albums]
    album_ids = []
    get_album_id = [album_ids.append( album['album']['album_id']) for album in album_data if album['album']['album_id'] not in album_ids]
    obj = dict(zip(albums, album_ids))
    return obj
    #return data
    
def get_album_tracks(album_id):
    res = requests.get(f'{BASE_URL}album.tracks.get', params={'album_id': album_id, 'apikey': API_SECRET_KEY})
    data = res.json()
    track_data = data['message']['body']['track_list']
    track_list = []
    tracks = [track_list.append( track['track']['track_name']) for track in track_data]
    ids = []
    track_ids = [ids.append(track['track']['track_id']) for track in track_data]
    obj = dict(zip(track_list, ids))

    return obj

def get_track_lyrics(track_id):
    res = requests.get(f'{BASE_URL}track.lyrics.get', params={'track_id': track_id, 'apikey': API_SECRET_KEY})
    data = res.json()
    lyrics = data['message']['body']['lyrics']['lyrics_body']
    copy = data['message']['body']['lyrics']['lyrics_copyright']
    return {'lyrics': lyrics, 'copyright':copy}