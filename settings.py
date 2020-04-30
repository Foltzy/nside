import os
import private

SECRET_KEY = private.SECRET_KEY

POSTGRES = {
    'user': private.DB_USERNAME,
    'pw': private.DB_PASSWORD,
    'db': private.DATABASE_NAME,
    'host': os.environ.get("DB_HOST", os.getenv('IP', '0.0.0.0')),
    'port': os.environ.get("DB_PORT", '5432')
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", True)

STARTING_ADMIN1 = private.STARTING_ADMIN1
STARTING_ADMIN_PASS = private.STARTING_ADMIN_PASS

# mail stuff
MAIL_SERVER = private.MAIL_SERVER
MAIL_PORT = private.MAIL_PORT
MAIL_USE_SSL = private.MAIL_USE_SSL
MAIL_USE_TLS = private.MAIL_USE_TLS
MAIL_USERNAME = private.MAIL_USERNAME
MAIL_PASSWORD = private.MAIL_PASSWORD
MAIL_DEFAULT_SENDER = private.ADMIN_EMAIL

# hashes
SECURITY_PASSWORD_HASH = private.SECURITY_PASSWORD_HASH
SECURITY_PASSWORD_SALT = private.SECURITY_PASSWORD_SALT

# controls what page you see after login
SECURITY_POST_LOGIN_VIEW = '/display' 
SECURITY_POST_CHANGE_VIEW = '/display' 
SECURITY_POST_RESET_VIEW = '/login' 

SECURITY_REGISTERABLE = os.environ.get("SECURITY_REGISTERABLE", True)
SECURITY_CONFIRMABLE = os.environ.get("SECURITY_CONFIRMABLE", True)
SECURITY_RECOVERABLE = os.environ.get("SECURITY_RECOVERABLE", True)
SECURITY_CHANGEABLE = os.environ.get("SECURITY_CHANGEABLE", True)
