import os
from dotenv import load_dotenv
# logging
import logging
from logging.config import dictConfig

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role # get my local objects

# setup logging config
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = create_app(os.getenv('FLASK_CONFIG') or 'settings')
migrate = Migrate(app, db)

# activate logging
root_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
handler = logging.FileHandler(root_path + '/nside/log.log', mode='a', encoding=None, delay=False)  # errors logged to this file
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)  # attach the handler to the app's logger
app.logger.info('App started.')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
