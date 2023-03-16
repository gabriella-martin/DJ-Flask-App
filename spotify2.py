import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials



class TrackRecommendations:

    def __init__(self,track_id):
        cid = config('SPOTIFY_CLIENT_ID')
        secret = config('SPOTIFY_CLIENT_SECRET')
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.track_id = track_id

    def get_recommendations(self):
        recommendations = self.sp.recommendations(seed_tracks =[self.track_id], limit=10)
        tracks = recommendations['tracks']
        track_ids = []
        for track in tracks:
            track_id = track['id']
            embed_url = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0'
            track_ids.append(embed_url)
        return track_ids
