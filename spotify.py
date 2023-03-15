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

    def get_track_details(self):

        '''song name, artists on the track & their id, song artwork, popularity, release year '''

        track_details = self.sp.track(self.track_id)
        song_name = track_details['name']
        artist_details = []
        artists = (track_details['artists'])
        for artist in artists:
            artist_name = artist['name']
            artist_id = artist['id']
            artist_details.append({'artist_name':artist_name, 'artist_id': artist_id})
        song_image = track_details['album']['images'][2]['url']
        release_year = (track_details['album']['release_date'])[:4]
        popularity = track_details['popularity']
        track_details = {'song_name': song_name, 'artists': artist_details, 'song_image': song_image, 'release_year': release_year, 'popularity':popularity}

        return track_details

    def get_audio_features(self):

        ''' danceability - Danceability describes how suitable a track is for dancing based on a combination of musical elements 
            including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is 
            most danceable.

            energy - Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, 
            energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on 
            the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, 
            and general entropy.

            instrumentalness - Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in 
            this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater 
            likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence 
            is higher as the value approaches 1.0.

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
        audio_features = {'danceability':danceability, 'energy': energy, 'key': key, 'instrumentalness':instrumentalness, 
                          'valence': valence, 'bpm': bpm}

        return audio_features

    def get_audio_analysis(self):

        '''tempo_confidence - the confidence, from 0.0 to 1.0, of the reliability of the tempo.
        key_confidence - The confidence, from 0.0 to 1.0, of the reliability of the key.'''
        audio_analysis = self.sp.audio_analysis(self.track_id)
        tempo_reliability = (audio_analysis['track']['tempo_confidence'])
        key_reliability = (audio_analysis['track']['key_confidence'])
        audio_analysis = {'tempo_reliability': tempo_reliability, 'key_reliability': key_reliability}
        return audio_analysis

taa = TrackAudioAnalysis('4zN21mbAuaD0WqtmaTZZeP')
taa.get_track_details()


