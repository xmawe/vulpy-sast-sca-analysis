#!/usr/bin/env python3

import os
from pathlib import Path

from flask import Flask, g, redirect, request
from flask_wtf.csrf import CSRFProtect

from mod_hello import mod_hello
from mod_user import mod_user
from mod_posts import mod_posts
from mod_mfa import mod_mfa
from mod_csp import mod_csp
from mod_api import mod_api

import libsession

app = Flask('vulpy')
# Use environment variable for SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(32).hex())
app.config['WTF_CSRF_TIME_LIMIT'] = None  # CSRF token doesn't expire

# Enable CSRF protection for all forms
csrf = CSRFProtect(app)

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')
app.register_blueprint(mod_csp, url_prefix='/csp')
app.register_blueprint(mod_api, url_prefix='/api')

csp_file = Path('csp.txt')
csp = ''

if csp_file.is_file():
    with csp_file.open() as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line = line.replace('\n', '')
            if line:
                csp += line
        print('CSP:', csp)

@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

@app.after_request
def add_security_headers(response):
    # CSP header
    if csp:
        response.headers['Content-Security-Policy'] = csp
    
    # Anti-clickjacking protection
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    return response

# Disable debug mode in production
app.run(debug=False, host='127.0.1.1', port=5001, extra_files='csp.txt')

