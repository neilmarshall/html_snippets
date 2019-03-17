from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    LoginUsername = StringField(label='Username', validators=[DataRequired()])
    LoginPassword = PasswordField(label='Password', validators=[DataRequired()])
    Submit = SubmitField(label="Login")


class RegistrationForm(FlaskForm):
    RegistrationUsername = StringField(label='Username', validators=[DataRequired()])
    RegistrationPassword = PasswordField(label='Password', validators=[DataRequired()])
    RegistrationPassword2 = PasswordField(label='Confirm password', validators=[DataRequired(),
        EqualTo('RegistrationPassword', message="Passwords do not match")])
    Identity = SelectField(label="Identity", choices=[
        ('None', 'None'), ('secret', 'Secret Identity'), ('public', 'Public Identity'), ('unknown', 'Identity Unknown'),
        ('known', 'Known to Authorities Identity'), ('no_dual', 'No Dual Identity')])
    Alignment = SelectField(label="Alignment", choices=[
        ('None', 'None'), ('bad', 'Bad Characters'), ('good', 'Good Characters'),
        ('neutral', 'Neutral Characters'), ('reformed', 'Reformed Criminals')])
    Gender = SelectField(label="Gender", choices=[
        ('None', 'None'), ('bisexual', 'Bisexual Characters'), ('genderfluid', 'Genderfluid Characters'),
        ('homosexual', 'Homosexual Characters'), ('pansexual', 'Pansexual Characters'),
        ('transgender', 'Transgender Characters'), ('transvestites', 'Transvestites')])
    Sex = SelectField(label="Sex", choices=[
        ('None', 'None'), ('agender', 'Agender Characters'), ('female', 'Female Characters'),
        ('genderfluid', 'Genderfluid Characters'), ('genderless', 'Genderless Characters'),
        ('male', 'Male Characters'), ('transgender', 'Transgender Characters')])            
    EyeColour = SelectField(label="Eye Colour", choices=[
        ('None', 'None'), ('amber', 'Amber Eyes'), ('auburn', 'Auburn Hair'), ('black', 'Black Eyeballs'),
        ('black', 'Black Eyes'), ('blue', 'Blue Eyes'), ('brown', 'Brown Eyes'), ('compound', 'Compound Eyes'),
        ('gold', 'Gold Eyes'), ('green', 'Green Eyes'), ('grey', 'Grey Eyes'), ('hazel', 'Hazel Eyes'),
        ('magenta', 'Magenta Eyes'), ('multiple', 'Multiple Eyes'), ('no', 'No Eyes'), ('one', 'One Eye'),
        ('orange', 'Orange Eyes'), ('photocellular', 'Photocellular Eyes'), ('pink', 'Pink Eyes'),
        ('purple', 'Purple Eyes'), ('red', 'Red Eyes'), ('silver', 'Silver Eyes'), ('variable', 'Variable Eyes'),
        ('violet', 'Violet Eyes'), ('white', 'White Eyes'), ('yellow', 'Yellow Eyeballs'), ('yellow', 'Yellow Eyes')])
    HairColour = SelectField(label="Hair Colour", choices=[
        ('None', 'None'), ('auburn', 'Auburn Hair'), ('bald', 'Bald'), ('black', 'Black Hair'),
        ('blond', 'Blond Hair'), ('blue', 'Blue Hair'), ('bronze', 'Bronze Hair'), ('brown', 'Brown Hair'),
        ('dyed', 'Dyed Hair'), ('gold', 'Gold Hair'), ('green', 'Green Hair'), ('grey', 'Grey Hair'),
        ('light', 'Light Brown Hair'), ('magenta', 'Magenta Hair'), ('no', 'No Hair'), ('orange', 'Orange Hair'),
        ('orange-brown', 'Orange-brown Hair'), ('pink', 'Pink Hair'), ('platinum', 'Platinum Blond Hair'),
        ('purple', 'Purple Hair'), ('red', 'Red Hair'), ('reddish', 'Reddish Blond Hair'),
        ('reddish', 'Reddish Brown Hair'), ('silver', 'Silver Hair'), ('strawberry', 'Strawberry Blond Hair'),
        ('variable', 'Variable Hair'), ('violet', 'Violet Hair'), ('white', 'White Hair'), ('yellow', 'Yellow Hair')])        
    Alive = SelectField(label="Alive", choices=[
        ('deceased', 'Deceased Characters'), ('living', 'Living Characters')])
    Appearances = IntegerField(label="Appearances", validators=[NumberRange(min=0, max=9999)])
    Submit = SubmitField(label="Register")

    def validate_RegistrationUsername(self, username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Please provide a unique username')
