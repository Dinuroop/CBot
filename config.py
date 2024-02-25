OPENAI_API_KEY = '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'
FIREBASE_API_KEY = 'AIzaSyC9XW-C5-eIFN07xQ5orz_4mvTvt0P2N5s'
FIREBASE_AUTH_DOMAIN = 'chatbot-1ba16.firebaseapp.com'
FIREBASE_DATABASE_URL = 'https://chatbot-1ba16.firebaseio.com'
SECRET_KEY = 'AIzaSyC9XW-C5-eIFN07xQ5orz_4mvTdf54vt0P2N5s'


class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = "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"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}
