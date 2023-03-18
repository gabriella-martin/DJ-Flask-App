import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials

#form_results = {'bpm_range': bpm_range, 'key_range':key_range, 'popularity':popularity, 'time_period':time_period, 'danceability':danceability, 'vocal':vocal, 'energy':energy, 'mood':mood}
#{'song_name': "Don't Stop Just Yet - VIP", 'artists': [{'artist_name': 'Belters Only', 'artist_id': '1H1sDUWSlytzifZTDpKgUA'}, {'artist_name': 'Jazzy', 'artist_id': '7zAAwgV5Wqmvpb4GzvlRkP'}], 'song_image': 'https://i.scdn.co/image/ab67616d00004851ff92c4f7dadc86a44a89e284', 'release_year': '2022', 'popularity': 42, 'danceability': 70, 'energy': 84, 'key': 11, 'vocal': 24, 'mood': 76, 'bpm': 127}
class TrackRecommendations():

    def __init__(self,track_id, form_results, track_details):
        cid = config('SPOTIFY_CLIENT_ID')
        secret = config('SPOTIFY_CLIENT_SECRET')
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.track_id = track_id
        self.form_results = form_results
        self.track_details = track_details

    def get_bpm_ranges(self):
        bpm_range = self.form_results['bpm_range']
        bpm_of_selected_track = self.track_details['bpm']
        if bpm_range == 'No preference':
            max_tempo = None
            min_tempo = None
        else:
            bpm_range = bpm_range[1:-1]
            max_tempo = bpm_of_selected_track + bpm_of_selected_track*bpm_range
            min_tempo = bpm_of_selected_track - bpm_of_selected_track*bpm_range
        return min_tempo, max_tempo
    
    def get_key_ranges(self):
        key_range = self.form_results['bpm_range']
        key_of_selected_track = self.track_details['key']
        if key_range == 'No preference':
            max_key = None
            min_key = None
        elif key_range == 'Same Key':
            max_key = key_of_selected_track
            min_key = key_of_selected_track
        else:
            if key_of_selected_track == 11:
                max_key = 0
                min_key = key_of_selected_track -1 
            if key_of_selected_track == 0:
                min_key = 11
                max_key = key_of_selected_track + 1
            else:
                min_key = key_of_selected_track -1
                max_key = key_of_selected_track +1
        return min_key, max_key

    def get_time_period(self):
        max_year = self.form_results['']





'''
lets consider options:

    BPM RANGE OPTIONS: +-3% +-5% +-8%
    KEY COMPLIMENTS: same key, complimentary key, dont care
    POPULARITY, DANCE, VOCAL, MOOD, ENERGY: more, less, don't care 

'''