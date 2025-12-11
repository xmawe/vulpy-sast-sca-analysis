#!/usr/bin/env python3

import os
from flask import Flask, g, redirect, request

from mod_hello import mod_hello
from mod_user import mod_user
from mod_posts import mod_posts
from mod_mfa import mod_mfa

import libsession

app = Flask('vulpy')
# Use environment variable for SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(32).hex())

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')


@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

# Disable debug mode in production and use proper cert paths
import tempfile
cert_dir = tempfile.gettempdir()
cert_path = os.path.join(cert_dir, 'acme.cert')
key_path = os.path.join(cert_dir, 'acme.key')

app.run(debug=False, host='127.0.1.1', ssl_context=(cert_path, key_path))
