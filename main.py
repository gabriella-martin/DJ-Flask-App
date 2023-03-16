from flask import Flask, render_template, request, redirect, url_for
from forms import SongInputForm
from decouple import config

from spotify import TrackAudioAnalysis
app = Flask(__name__)

app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')

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
    popularity = track_details['popularity']
    release_year = track_details['release_year']

    audio_features = taa.get_audio_features()
    
    if request.method == 'POST':
        if request.form['yesorno'] == 'Yes':
            return redirect(url_for('set_page'))
        else :
            return redirect(url_for('home'))
    return render_template('song.html', url=url, popularity=popularity, release_year=release_year, audio_features=audio_features)

@app.route('/set')
def set_page():

    return render_template('set.html')

if __name__ == '__main__':
    app.run(debug=True, port=5800)