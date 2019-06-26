from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_admin import Admin

security = Security()
db = SQLAlchemy()
admin = Admin(name='Virtuality Admin', template_mode='bootstrap3')