from authomatic.providers import oauth2

CONFIG = {

    'fb': {

        'class_': oauth2.Facebook,
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1802374583354393',
        'consumer_secret': '439f9b7fbe5689e5f4c9d6427ff30d17',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },

}