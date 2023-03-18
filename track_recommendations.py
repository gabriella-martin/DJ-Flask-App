import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials

# python3 track_recommendations.py

class TrackRecommendations():

    def __init__(self,track_id, form_results, track_features):
        cid = config('SPOTIFY_CLIENT_ID')
        secret = config('SPOTIFY_CLIENT_SECRET')
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.track_id = track_id
        self.form_results = form_results
        self.track_features = track_features
    def get_bpm_ranges(self):
        bpm_range = self.form_results['bpm_range']
        bpm_of_selected_track = self.track_features['bpm']
        if bpm_range == 'No Preference':
            max_tempo = 'NULL'
            min_tempo = 'NULL'
        else:
            bpm_range = int(bpm_range[1:-1])
            max_tempo = bpm_of_selected_track + bpm_of_selected_track*bpm_range
            min_tempo = bpm_of_selected_track - bpm_of_selected_track*bpm_range
        tempo = [min_tempo, max_tempo]
        
        return tempo
    
    def get_key_ranges(self):
        key_range = self.form_results['key_range']
        key_of_selected_track = self.track_features['key']
        if key_range == 'No Preference':
            max_key = 'NULL'
            min_key = 'NULL'
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
        key = [min_key, max_key]

        return key

    def get_popularity_range(self):
        popularity_of_selected_track = self.track_features['popularity']
        popularity = self.form_results['popularity']
        if popularity == 'No Preference':
            max_popularity = 'NULL'
            min_popularity = 'NULL'
        elif popularity == 'More Popular':
            min_popularity = popularity_of_selected_track
            max_popularity = 'NULL'
        else:
            max_popularity = popularity_of_selected_track
            min_popularity = 'NULL'
        popularity = [min_popularity, max_popularity]
        return popularity


    def get_danceability_range(self):
        danceability_of_selected_track = self.track_features['danceability']
        danceability = self.form_results['danceability']
        if danceability == 'No Preference':
            max_danceability = 'NULL'
            min_danceability = 'NULL'
        elif danceability == 'More Danceable':
            min_danceability = danceability_of_selected_track
            max_danceability = 'NULL'
        else:
            max_danceability = danceability_of_selected_track
            min_danceability = 'NULL'
        danceability = [min_danceability, max_danceability]
        return danceability
    def get_energy_range(self):
        energy_of_selected_track = self.track_features['energy']
        energy = self.form_results['energy']
        if energy == 'No Preference':
            max_energy = 'NULL'
            min_energy = 'NULL'
        elif energy == 'More Energy':
            min_energy = energy_of_selected_track
            max_energy = 'NULL'
        else:
            max_energy = energy_of_selected_track
            min_energy = 'NULL'
        energy = [min_energy, max_energy]
        return energy

    def get_mood_range(self):
        mood_of_selected_track = self.track_features['mood']
        mood = self.form_results['mood']
        if mood == 'No Preference':
            max_mood = 'NULL'
            min_mood = 'NULL'
        elif mood == 'Happier':
            min_mood = mood_of_selected_track
            max_mood = 'NULL'
        else:
            max_mood = mood_of_selected_track
            min_mood = 'NULL'

        mood = [min_mood, max_mood]
        return mood
    
    def get_recommendations(self):
        tempo = self.get_bpm_ranges()
        key = self.get_key_ranges()
        popularity = self.get_popularity_range()
        danceability = self.get_danceability_range()
        energy = self.get_energy_range()
        mood = self.get_mood_range()

        preferences_list = tempo + key + popularity + danceability + energy + mood
        for index, preference in enumerate(preferences_list):
            if preference == 'NULL':
                preferences_list[index] = None

        recommendations = self.sp.recommendations(seed_tracks =[self.track_id], min_tempo=preferences_list[0], max_tempo=preferences_list[1], min_key=preferences_list[2],
                                                  max_key=preferences_list[3], max_popularity=preferences_list[4], min_popularity=preferences_list[5],
                                                   min_danceability=preferences_list[6],
                                                  max_danceability=preferences_list[7], min_energy=preferences_list[8], max_energy=preferences_list[9], min_valence = preferences_list[10],
                                                  max_valence=preferences_list[11], limit=10)
        
        urls = []
        tracks = recommendations['tracks']
        for track in tracks:
            track_id = track['id']
            track_embed_link = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0'
            urls.append(track_embed_link)

        return urls

