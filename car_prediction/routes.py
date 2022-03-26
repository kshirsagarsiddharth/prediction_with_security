from car_prediction import server
from flask_login import current_user, login_required, logout_user
from flask_dance.contrib.google import google 
from flask_dance.contrib.github import github
from flask import render_template, jsonify, url_for, redirect, request
from car_prediction.oauth import github_blueprint, google_blueprint
server.register_blueprint(github_blueprint, url_prefix = '/github_login')
server.register_blueprint(google_blueprint, url_prefix = '/google_login')



@server.route("/")
def home():
    return render_template('index.html', current_user=current_user)


@server.route('/ping')
@login_required
def ping():
    return jsonify(ping='pong')



@server.route('/github')
def github_login():
    # if current_user.is_authenticated:
    #     res = github.get("/user")
    #     return render_template('landing.html', username=res.json()['login'])
    if not github.authorized:
        return redirect(url_for('github.login'))
    # res = github.get("/user")
    # return render_template('landing.html', username=res.json()['login'])


@server.route('/google')
def google_login():
    # if current_user.is_authenticated:
    #     response = google.get('/oauth2/v2/userinfo')
    #     response_json = response.json()
    #     return render_template('landing.html', username=response_json['email'])

    if not google.authorized:
        return redirect(url_for('google.login'))


@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


