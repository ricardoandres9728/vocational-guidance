SECRET_KEY = "b!NxacM: !x11x00xcbyx0fxcdx11xa8 + 0x16z3xc0Um1xd0"
DEBUG = True
HOSTNAME = 'http://0.0.0.0:5000'
DATABASE_HOST = 'localhost'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'michi2006'
DATABASE_NAME = 'Vocacional'
DB_URI = "postgresql://%s:%s@%s/%s" % (DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = "C:\\Users\\ricar\\Documents\\Repositorio\\vocational-guidance\\static\\images"
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
EMAIL_TIMEOUT = 30
MAIL_USE_SSL = False
MAIL_USERNAME = 'cuboarisma2017@gmail.com'
MAIL_PASSWORD = 'Arisma2017'
