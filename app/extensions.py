from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_admin import Admin
from flask_migrate import Migrate
from flask_mail import Mail

security = Security()
db = SQLAlchemy()
admin = Admin(name='nside admin', template_mode='bootstrap3')
mail = Mail()
migrate = Migrate()