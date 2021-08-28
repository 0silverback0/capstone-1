from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class AddArtist(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    img_url = StringField('image URL')

class Signup(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    img_url = StringField('Image URL')

class Login(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PostForm(FlaskForm):
    text = StringField('Post')

class Edit(FlaskForm):
     username = StringField('Name')
     img_url = StringField('Image URL')
    
