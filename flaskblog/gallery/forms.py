from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class UploadPictureForm(FlaskForm):#this registration inherits from flaskform
    pictures = MultipleFileField('Select Pictures', validators=[FileAllowed(['jpg', 'png', 'zip'])])
    description = TextAreaField('Describe your picture(s)!')
    submit = SubmitField('Upload')


class SearchForm(FlaskForm):
    search = StringField('Search the gallery!')