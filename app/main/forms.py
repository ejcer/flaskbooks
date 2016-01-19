from flask.ext.wtf import Form
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import StringField, TextAreaField, BooleanField, SubmitField

class ContactForm(Form):
    name = StringField('What\'s your name?', validators=[Length(0, 64)])
    email = StringField('And, your email address, please?', validators=[Required(), Length(1, 64), Email()])
    contact_req = TextAreaField('How may I be of assistance?')
    submit = SubmitField('Let\'s do business!')

class LoginForm(Form):
    password = StringField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class PostForm(Form):
    title = StringField('title', validators=[Required()])
    body = TextAreaField('new body', validators=[Required()])
    published = BooleanField('published')
    submit = SubmitField('Submit')
