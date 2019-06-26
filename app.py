from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db, security, admin
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore, utils, Security
from stem.models import User, Role, College, Building, Room, ResidentOf, PostAdmin, UserAdmin
import private

# app
app = Flask(__name__)
app.config.from_object('settings')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# add (app) to sqlalchemy 
db.init_app(app)
security.init_app(app, user_datastore)

# add (app) to flask admin
admin.init_app(app)
# flask admin views
admin.add_view(PostAdmin(Role, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(College, db.session))
admin.add_view(PostAdmin(Building, db.session))
admin.add_view(PostAdmin(Room, db.session))
admin.add_view(PostAdmin(ResidentOf, db.session))


# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app routes
from stem.views import *

# executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # create any database tables that don't exist yet.
    db.create_all()

    # create the admin role
    user_datastore.find_or_create_role(name='admin')

    # create admin user  
    encrypted_password = utils.encrypt_password(private.STARTING_ADMIN_PASS)
    if not user_datastore.get_user(private.STARTING_ADMIN1):
        user_datastore.create_user(first_name="admin", last_name="NULL", email=private.STARTING_ADMIN1, password=encrypted_password)

    db.session.commit()

    # add admin to user above
    user_datastore.add_role_to_user(private.STARTING_ADMIN1, 'admin')

    db.session.commit()

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=int('5000'),
        debug=app.config['DEBUG']
    )


