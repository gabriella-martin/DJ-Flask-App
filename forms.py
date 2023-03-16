from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SongInputForm(FlaskForm):
    song = StringField('Song Name',
                           validators=[DataRequired()])
    artist = StringField('Artist',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


