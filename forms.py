from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired


class SongInputForm(FlaskForm):
    song = StringField('Song Name:',
                           validators=[DataRequired()])
    artist = StringField('Artist:',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


class PersonalisationForm(FlaskForm):
    bpm_range = SelectField('What BPM range?', choices=['±5%', '±7%', 'No Preference'])
    key_range = SelectField('What key range?', choices = ['Same Key', 'Complimentary Key', 'No Preference'])
    max_year = SelectField('Max year', choices = ['Past 3 Years', 'Past Decade', "2000's", "<2000's"])
    popularity = SelectField('What popularity range?', choices = ['No Preference', 'Less Popular', 'More Popular'])
    danceability= SelectField('What popularity range?', choices = ['No Preference', 'Less Danceable', 'More Danceable'])
    vocal= SelectField('What popularity range?', choices = ['No Preference', 'Less Vocal', 'More Vocal'])
    energy= SelectField('What popularity range?', choices = ['No Preference', 'Less Energy', 'More Energy'])
    mood= SelectField('What popularity range?', choices = ['No Preference', 'Sadder', 'Happier'])