SECRET_KEY = "b!NxacM: !x11x00xcbyx0fxcdx11xa8 + 0x16z3xc0Um1xd0"
DEBUG = True
HOSTNAME = 'http://0.0.0.0:5000'
DATABASE_HOST = '67.205.175.15'
DATABASE_USER = 'wizybit'
DATABASE_PASSWORD = 'Michi2006.'
DATABASE_NAME = 'Vocacional'
DATABASE_PORT = '5432'
DB_URI = "postgresql://%s:%s@%s:%s/%s" % (DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
