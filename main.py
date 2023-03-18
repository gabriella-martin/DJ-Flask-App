from flask import Flask, render_template, request, redirect, url_for
from forms import SongInputForm, PersonalisationForm
from decouple import config

from track_analysis import TrackAudioAnalysis

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
    track_features = track_details | audio_features
    print(track_features)
    form = PersonalisationForm()
    if request.method == 'POST':
        bpm_range = (request.form['bpm_range'])
        key_range = request.form['key_range']
        popularity = request.form['popularity']
        time_period= request.form['time_period']
        danceability= request.form['danceability']
        vocal= request.form['vocal']
        energy= request.form['energy']
        mood= request.form['mood']
        form_results = {'bpm_range': bpm_range, 'key_range':key_range, 'popularity':popularity, 'time_period':time_period, 'danceability':danceability, 'vocal':vocal, 'energy':energy, 'mood':mood}
        return redirect(url_for('set_page', track_id=track_id, form_results=form_results))
    return render_template('song.html', url=url, track_features=track_features, form=form)

@app.route('/set/<track_id>/<form_results>')
def set_page(track_id, form_results):
    print(form_results)

    return render_template('set.html', form=form_results)

if __name__ == '__main__':
    app.run(debug=True, port=5800)