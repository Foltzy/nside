# app/__init__.py
# imports
from flask import Flask, render_template, url_for
from flask_security import SQLAlchemyUserDatastore, utils
import os
from datetime import datetime

from .extensions import db, security, mail, migrate, admin
from .main.forms import RegisterForm
from .models import User, Role, College, Building, Room, ResidentOf, PostAdmin, UserAdmin


# error handling -- err
def crash_page(e):
    return render_template('main/500.html'), 500

def page_not_found(e):
    return render_template('main/404.html'), 404

def page_forbidden(e):
    return render_template('main/403.html'), 403



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


    # blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)   

    # error handlers -- err
    # calls from above
    app.register_error_handler(500, crash_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)

    
    # custom filters -- fil
    def get_user_by_user_key(user_key):
        # your logic code here, e.g.
        user = user_datastore.find_user(id=user_key)
        if user.first_name:
            return user.first_name + " " + user.last_name
        else:
            return "Anonymous"

    app.jinja_env.filters['get_name_by_key'] = get_user_by_user_key

    # executes before the first request is processed
    @app.before_first_request
    def before_first_request():

        # create any db that doesn't exist
        db.create_all()

        # create roles -- admin (main), student, parent, dean
        user_datastore.find_or_create_role(name='admin')
        user_datastore.find_or_create_role(name='end-user')
        user_datastore.find_or_create_role(name='dean')
        user_datastore.find_or_create_role(name='parent')
        user_datastore.find_or_create_role(name='student')

        # create management users 
        encrypted_password = utils.encrypt_password(app.config['STARTING_ADMIN_PASS'])
        if not user_datastore.get_user(app.config['STARTING_ADMIN1']):
            user_datastore.create_user(email=app.config['STARTING_ADMIN1'], password=encrypted_password, first_name='admin', last_name='user')

        if not user_datastore.get_user('ryane@gilmour.org'):
            user_datastore.create_user(email='ryane@gilmour.org', password='ryane', first_name='Ed', last_name='Ryan')
     
        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()


        # TODO: Make more DRY
        # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
        # Users already have these Roles.) Again, commit any database changes.
        user_datastore.add_role_to_user(app.config['STARTING_ADMIN1'], 'admin')
        confirmed_admin = user_datastore.get_user(app.config['STARTING_ADMIN1'])
        if not confirmed_admin.confirmed_at:
            confirmed_admin.confirmed_at = datetime.utcnow()

        user_datastore.add_role_to_user('ryane@gilmour.org', 'dean')
        confirmed_dean = user_datastore.get_user('ryane@gilmour.org')
        if not confirmed_dean.confirmed_at:
            confirmed_dean.confirmed_at = datetime.utcnow()

        db.session.commit()
    
    return app
