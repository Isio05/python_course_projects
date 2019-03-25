from user import User
from database import Database
import twitter_utils

# Created for testing purposes
Database.initialise()
user_email = input('What is your email? ')
logged_user = User.load_from_db_by_email(user_email)

if logged_user is None:
    request_token = twitter_utils.get_request_token()
    oauth_verifier = twitter_utils.get_oauth_verifier(request_token)
    access_token = twitter_utils.get_access_token(request_token, oauth_verifier)

    data_for_dict = ['email', 'first_name', 'last_name', 'oauth_token', 'oauth_token_secret', 'id']
    user_data = dict.fromkeys(data_for_dict, '<empty>')
    user_data['email'] = user_email
    user_data['first_name'] = str(input('Type in your first name: '))
    user_data['last_name'] = str(input('Type in your last name: '))
    user_data['oauth_token'] = access_token['oauth_token']
    user_data['oauth_token_secret'] = access_token['oauth_token_secret']
    user_data['id'] = None

    new_user = User(**user_data)

    new_user.save_to_db()
    print('Account created, you need to restart the program.')

elif logged_user:
    tweets = logged_user.twitter_request(uri='https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

    for tweet in tweets['statuses']:
        print(tweet['text'])
