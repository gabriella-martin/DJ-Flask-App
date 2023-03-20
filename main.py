from flask import Flask, render_template, request, redirect, url_for, session
from forms import SongInputForm, PersonalisationForm
from dotenv import load_dotenv
import os
load_dotenv()

from spotify_api_pipelines.track_analysis import TrackAudioAnalysis
from spotify_api_pipelines.track_recommendations import TrackRecommendations
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# python3 main.py 

@app.route('/', methods=['GET','POST'])
def home():
    form = SongInputForm()
    if request.method == 'POST' and form.validate():
        search_query = request.form['song'] + request.form['artist']
        track_id = (TrackAudioAnalysis(search_query)).track_id
        return redirect(url_for('song_page', track_id=track_id))
    return render_template('index.html', form=form)


@app.route('/song/<track_id>', methods=['GET','POST'] )
def song_page( track_id):
    url = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0'
    track_features = (TrackAudioAnalysis(track_id=track_id)).format_track_details()
    form = PersonalisationForm()
    if request.method == 'POST':
        form_results = request.form
        session['form_results'] = form_results
        return redirect(url_for('set_page', track_id=track_id))
    return render_template('song.html', url=url, track_features_formatted=track_features, form=form)

@app.route('/set/<track_id>', methods =['GET','POST'])
def set_page( track_id):
    form_results = session.get('form_results')
    track_features_unformatted = (TrackAudioAnalysis(track_id=track_id)).get_unformatted_track_details()
    tr = TrackRecommendations(track_id=track_id, form_results=form_results, track_features=track_features_unformatted)
    urls = tr.get_recommendations()
    if request.method == 'POST':
        form_results = request.form
        try:
            url = form_results['seed']
            new_seed_track_id = url[37:-29]
            return redirect(url_for('song_page', track_id=new_seed_track_id))
        except KeyError:
            url = form_results['set']
    return render_template('set.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)