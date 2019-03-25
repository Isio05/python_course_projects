import oauth2
import urllib.parse as urlparse


class TwitterConsoleLogin:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer = oauth2.Consumer(consumer_key, consumer_secret)

    def complete_login(self):
        request_token = self.__get_request_token()
        verifier = self.__get_oauth_verifier(request_token)
        return self.__get_access_token(request_token, verifier)

    def __get_request_token(self):
        client = oauth2.Client(self.consumer)

        response, content = client.request('https://api.twitter.com/oauth/request_token')
        if response.status != 200:
            print("An error occurred when accessing Twitter.")

        return dict(urlparse.parse_qsl(content.decode('utf-8')))

    def __get_oauth_verifier(self, request_token):
        print('Go to following site to generate access token:')
        print(self.__get_oauth_verifier_url(request_token))

        return input("Enter the PIN code.")

    def __get_oauth_verifier_url(self, request_token):
        return '{}?oauth_token={}'.format('https://api.twitter.com/oauth/authorize', request_token['oauth_token'])

    def __get_access_token(self, request_token, oauth_verifier):
        token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth2.Client(self.consumer, token)

        response, content = client.request('https://api.twitter.com/oauth/access_token', 'POST')
        return dict(urlparse.parse_qsl(content.decode('utf-8')))


twitter_login = TwitterConsoleLogin('7loPML9vbTgWd9uBnPVRcn8eK', 'RaPVLE5KJ3kmj3VjlsOirjull5eA9T0GkYJVSFgNmKttLAYhTj')
twitter_login.complete_login()
