import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
import os
# python3 spotify.py


class TrackAudioAnalysis:

    def __init__(self,search_query=None, track_id=None):
        cid = os.getenv('SPOTIFY_CLIENT_ID')
        secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        if search_query:
            song_search = self.sp.search(search_query, limit=1)
            self.track_id = song_search['tracks']['items'][0]['id']
        else:
            self.track_id = track_id
        self.embed_url = f'https://open.spotify.com/embed/track/{self.track_id}?utm_source=generator&theme=0'

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
        danceability =audio_features[0]['danceability']
        energy = audio_features[0]['energy']
        key = audio_features[0]['key']
        instrumentalness = audio_features[0]['instrumentalness']
        valence = audio_features[0]['valence']
        bpm = audio_features[0]['tempo']
        audio_features = {'danceability':danceability, 'energy': energy, 'key': key, 'vocal':instrumentalness, 
                          'mood': valence, 'bpm': bpm}

        return audio_features
    
    def get_unformatted_track_details(self):
        track_details = self.get_track_details()
        audio_features = self.get_audio_features()
        track_features = track_details | audio_features
        return track_features
    
    def format_track_details(self):
        track_features = self.get_unformatted_track_details()
        track_features['danceability'] = round((track_features['danceability'])*100)
        track_features['energy'] = round((track_features['energy'])*100)
        track_features['mood'] = round((track_features['mood'])*100)
        track_features['vocal'] = round((1-track_features['vocal'])*100)
        track_features['bpm'] = round(track_features['bpm'])   
        return track_features





