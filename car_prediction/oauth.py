import os 
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint 
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage 
from car_prediction.models import User, Oauth
from car_prediction import db , server
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound 
from flask_dance.consumer import oauth_authorized 


os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GITHUB_CLIENT_ID = server.config['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = server.config['GITHUB_CLIENT_SECRET']

github_blueprint = make_github_blueprint(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET, 
    storage=SQLAlchemyStorage(
        Oauth,
        db.session,
        user=current_user,
        user_required=False
    )
)


GOOGLE_CLIENT_ID = server.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = server.config['GOOGLE_CLIENT_SECRET']

google_blueprint = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET, 
    storage=SQLAlchemyStorage(
        Oauth,
        db.session,
        user=current_user,
        user_required=False
    ),
    scope=['profile','email'],
    offline=True
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint,token):
    info = blueprint.session.get('/user')
    if info.ok:
        account_info = info.json()
        username = account_info['login']
        query = User.query.filter_by(username = username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username = username)
            db.session.add(user)
            db.session.commit()
        login_user(user)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint,token):
    info = blueprint.session.get('/oauth2/v2/userinfo')
    if info.ok:
        account_info = info.json()
        username = account_info['email']
        query = User.query.filter_by(username = username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username = username)
            db.session.add(user)
            db.session.commit()
        login_user(user)



