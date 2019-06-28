from flask import Flask, render_template, url_for
from flask_security import SQLAlchemyUserDatastore, utils
import os
from datetime import datetime

from .extensions import db, security, mail, migrate, admin
from .main.forms import RegisterForm
from .models import User, Role, College, Building, Room, ResidentOf, PostAdmin, UserAdmin

# sort of like an application factory
def create_app(config_name):
    # Initialize Flask and set some config values
    app = Flask(__name__)
    app.config.from_object(config_name)
    
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, confirm_register_form=RegisterForm)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Add Flask-Admin views for Users and Roles
    admin.init_app(app)
    admin.add_view(PostAdmin(Role, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(PostAdmin(College, db.session))
    admin.add_view(PostAdmin(Building, db.session))
    admin.add_view(PostAdmin(Room, db.session))
    admin.add_view(PostAdmin(ResidentOf, db.session))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)   

    ################
    # CUSTOM FILTERS
    # Example:
    # https://stackoverflow.com/questions/19394844/how-to-get-the-user-object-from-the-user-key-in-flask-template
    def get_user_by_user_key(user_key):
        # your logic code here, e.g.
        user = user_datastore.find_user(id=user_key)
        if user.first_name:
            return user.first_name + " " + user.last_name
        else:
            return "Anonymous"

    app.jinja_env.filters['get_name_by_key'] = get_user_by_user_key

    # Executes before the first request is processed.
    @app.before_first_request
    def before_first_request():

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "end-user" -- unless they already exist
        user_datastore.find_or_create_role(name='admin')
        user_datastore.find_or_create_role(name='end-user')

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the password.
        encrypted_password = utils.encrypt_password(app.config['STARTING_ADMIN_PASS'])
        if not user_datastore.get_user(app.config['STARTING_ADMIN1']):
            user_datastore.create_user(email=app.config['STARTING_ADMIN1'], password=encrypted_password)
     
        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()


        # TODO: Make more DRY
        # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
        # Users already have these Roles.) Again, commit any database changes.
        user_datastore.add_role_to_user(app.config['STARTING_ADMIN1'], 'admin')
        confirmed_admin = user_datastore.get_user(app.config['STARTING_ADMIN1'])
        if not confirmed_admin.confirmed_at:
            confirmed_admin.confirmed_at = datetime.utcnow()

        db.session.commit()
    
    return app
