from flask import Flask, render_template, request, redirect, url_for, session
from forms import SongInputForm, PersonalisationForm
from decouple import config

from track_analysis import TrackAudioAnalysis
from track_recommendations import TrackRecommendations
app = Flask(__name__)

app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# python3 main.py 

@app.route('/', methods=['GET','POST'])
def home():
    form = SongInputForm()
    if request.method == 'POST' and form.validate():
        song = request.form['song']
        artist = request.form['artist']
        search_query = song + artist
        taa = TrackAudioAnalysis(search_query)
        track_id = taa.track_id
        return redirect(url_for('song_page', search_query=search_query, track_id=track_id))
    return render_template('index.html', form=form)


@app.route('/song/<search_query>/<track_id>', methods=['GET','POST'] )
def song_page(search_query, track_id):
    url = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0'
    taa = TrackAudioAnalysis(search_query)
    track_details = taa.get_track_details()
    audio_features = taa.get_audio_features()
    track_features_formatted= track_details | audio_features
    track_features_formatted['danceability'] = round((track_features_formatted['danceability'])*100)
    track_features_formatted['energy'] = round((track_features_formatted['energy'])*100)
    track_features_formatted['mood'] = round((track_features_formatted['mood'])*100)
    track_features_formatted['vocal'] = round((1-track_features_formatted['vocal'])*100)
    track_features_formatted['bpm'] = round(track_features_formatted['bpm'])    
    form = PersonalisationForm()
    if request.method == 'POST':
        form_results = request.form
        session['form_results'] = form_results
        return redirect(url_for('set_page', track_id=track_id, search_query=search_query))
    return render_template('song.html', url=url, track_features_formatted=track_features_formatted, form=form)

@app.route('/set/<search_query>/<track_id>', methods =['GET'])
def set_page(search_query, track_id):
    form_results = session.get('form_results')
    taa = TrackAudioAnalysis(search_query)
    track_details = taa.get_track_details()
    audio_features = taa.get_audio_features()
    track_features_unformatted= track_details | audio_features
    tr = TrackRecommendations(track_id=track_id, form_results=form_results, track_features=track_features_unformatted)
    urls = tr.get_recommendations()
    return render_template('set.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True, port=5800)