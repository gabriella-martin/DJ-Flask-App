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
        search_query = taa.track_id
        return redirect(url_for('song_page', song_query=search_query))
    return render_template('index.html', form=form)


@app.route('/<song_query>', methods=['GET','POST'] )
def song_page(song_query):
    url = f'https://open.spotify.com/embed/track/{song_query}?utm_source=generator&theme=0'
    return render_template('song.html', url=url)



if __name__ == '__main__':
    app.run(debug=True, port=5800)