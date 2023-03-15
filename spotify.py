import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials

# python3 spotify.py

class TrackAudioAnalysis:

    def __init__(self,track_id):
        cid = config('SPOTIFY_CLIENT_ID')
        secret = config('SPOTIFY_CLIENT_SECRET')
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.track_id = track_id

    def get_audio_features(self):
        '''
            danceability - Danceability describes how suitable a track is for dancing based on a combination of musical elements 
            including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is 
            most danceable

            energy - Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, 
            energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on 
            the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, 
            and general entropy

            instrumentalness - Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in 
            this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater 
            likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence 
            is higher as the value approaches 1.0

            valence - A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound
            more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
        '''

        audio_features = self.sp.audio_features(self.track_id)
        danceability = audio_features[0]['danceability']
        energy = audio_features[0]['energy']
        key = audio_features[0]['key']
        instrumentalness = audio_features[0]['instrumentalness']
        valence = audio_features[0]['valence']
        bpm = audio_features[0]['tempo']
        audio_features = [danceability, energy, key, instrumentalness, valence, bpm]
        for i in audio_features:
            print(i)


'''ya = sp.recommendations(seed_tracks = ['4D2uN3J3sjKL3TUrvY0pS7'])
print(ya)'''


taa = TrackAudioAnalysis('4zN21mbAuaD0WqtmaTZZeP')
taa.get_audio_features()


