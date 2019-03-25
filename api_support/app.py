from flask import Flask, render_template, session, redirect, request, url_for, g
import twitter_utils
from user_flask import User
from database import Database
from constants import SECRET_KEY
import requests

Database.initialise()

app = Flask(__name__, template_folder='Templates')
app.secret_key = SECRET_KEY


@app.before_request
def load_user():
    """Check for user in session and load details from db if present"""
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/login/twitter')
def twitter_login():
    """Init login with tweeter procedure and save token"""
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = twitter_utils.get_request_token()
    session['request_token'] = request_token

    return redirect(twitter_utils.get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = twitter_utils.get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    """Gather posts requested by user and mark them basing on the sentiment analysis"""
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label':'neutral'} for tweet in tweets['statuses']]
    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        response_json = r.json()
        tweet['label'] = response_json['label']

    return render_template('search.html', content=tweet_texts)


app.run(port=4995, debug=True)
