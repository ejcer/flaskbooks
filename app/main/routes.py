from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Post, Subscriber
from forms import ContactForm
from ..email import send_email
from . import main

@main.route('/about', methods=['GET'])
@main.route('/', methods=['GET'])
def index():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        app = current_app._get_current_object()
        send_email(app.config['FLASKY_ADMIN'], \
            'Assistance Request [edwardmcenrue.com]', \
            'email/contact_req', \
            name=form.name.data, \
            email=form.email.data, \
            contact_req=form.contact_req.data)
        return redirect(url_for('.contact'))
    return render_template('contact.html', form=form)

@main.route('/writing', methods=['GET'])
def writing():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('writing.html', posts=posts)
