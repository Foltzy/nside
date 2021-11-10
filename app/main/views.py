# views.py
from flask import Flask, request, render_template, flash, redirect, \
    url_for, jsonify, current_app
from flask_security import current_user, utils, roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_mail import Message
from flask_security import SQLAlchemyUserDatastore
# files
from .forms import LoginForm, RegisterForm, AddStudentForm, ContactForm
from . import main as app
from .. import db, mail
from ..models import College, Building, Room, ResidentOf, User, Role

import json
import private


# ######################################################
#    LANDING
# ###################################################### 
@app.route('/')
@app.route('/index/')
def index():
    form = ContactForm()
    return render_template('stem/index.html', form=form)

# ====================
# ========== for students
@app.route('/students')
def students():
    form = ContactForm()
    return render_template('landing/students.html', form=form)

# ====================
# ========== for parents
@app.route('/parents')
def parents():
    return render_template('landing/parents.html')

# ====================
# ========== for schools
@app.route('/schools')
def schools():
    return render_template('landing/schools.html')

# ====================
# ========== about us
@app.route('/aboutus')
def about_us():
    form = ContactForm()
    return render_template('landing/about_us.html', form=form)


















# ######################################################
#    NEW WITH TEMPLATE
# ###################################################### 
# ====================
# ========== new display page (w/ template)
@app.route('/displayland')
@login_required
def displayland():

    # FIND THE ROOM THE USER IS LINKED TO
    # see if the  user is linked  to a room if not set to 'None'
    # todo[p]: have a fail safe in place to catch users that don't have a linked room
    if len(current_user.rooms) != 0:
        linked_room = current_user.rooms[0]
    else:
        linked_room = None

    return render_template('landing/display.html', linked_room=linked_room)

# ====================
# ========== new dean panel (w/ template)
@app.route('/deanland')
@roles_required('dean')
def deanland():
    all_students = User.query.filter_by(student=True).all()
    all_parents = User.query.filter_by(parent=True).all()
    all_deans = User.query.filter_by(dean=True).all()
    all_users = all_students + all_parents + all_deans
    name = current_user.first_name

    return render_template('landing/dean_panel.html', name=name, users=all_users)    
    

# ====================
# ========== new dean panel (w/ template)
@app.route('/studentland/', methods=('GET', 'POST'))
@roles_required('dean')
def studentland():
    form = AddStudentForm()
    name = current_user.first_name

    # for select2 fields
    colleges = College.query.all()
    buildings = Building.query.all()

    # query all rooms in database for selectfield
    form.room_id.choices = [(str(room.id), repr(room)) for room in Room.query.all()]

    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name =  form.last_name.data
        email = form.email.data
        password = form.password.data
        student = form.student.data
        parent = form.parent.data
        dean = form.dean.data
        confirmed_at = datetime.utcnow()

        user = User(first_name=first_name, last_name=last_name, email=email, password=password, student=student, parent=parent, dean=dean, confirmed_at=confirmed_at)
        db.session.add(user)
        db.session.commit()


        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        if user.student == True:
            user_datastore.add_role_to_user(user.email, 'student')
        elif user.parent == True:
            user_datastore.add_role_to_user(user.email, 'parent')
        elif user.dean == True:
            user_datastore.add_role_to_user(user.email, 'dean')
        else: 
            flash("You must select a role", 'warning')
            return redirect(url_for('main.deanland'))

        db.session.commit()

        
        relationship = ResidentOf()
        relationship.user_id = user.id
        if form.room_id.data != "Room":
            relationship.room_id = form.room_id.data
        else:
            relationship.room_id = None

        db.session.add(relationship)
        db.session.commit()

        flash("Added " + form.first_name.data + " " + form.last_name.data, 'success')
        return redirect(url_for('main.deanland'))

    return render_template('landing/add_user.html', form=form, colleges=colleges, buildings=buildings, name=name, action="new")

# ====================
# ========== delete user
@app.route('/user/delete/s<int:user_id>')
@roles_required('dean')
def deleteuser(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash("User " + user.first_name + " " + user.last_name + " deleted", 'success')
    return redirect(url_for('main.deanland'))

# ====================
# ========== new edit user (w/ template)
@app.route('/editland')
def editland():
    return render_template('landing/edit_user.html')















































# ######################################################
#    GA /STEM
# ###################################################### 
# ====================
# ========== display
@app.route('/display/')
@login_required
def display():
    # select2 field queries
    colleges = College.query.all()
    buildings = Building.query.all()
    all_rooms = Room.query.all()

    name = current_user.first_name + " " + current_user.last_name

    # see if the  user is linked  to a room if not set to 'None'
    # todo[p]: have a fail safe in place to catch users that don't have a linked room
    if len(current_user.rooms) != 0:
        linked_room = current_user.rooms[0]
    else:
        linked_room = None

    return render_template('stem/display.html', name=name, linked_room=linked_room, colleges=colleges, buildings=buildings, rooms=all_rooms)

# ====================
# ========== login
@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if utils.verify_password(form.password.data, user.password):
                login_user(user)

                return redirect(request.args.get('next') or url_for('main.display'))
        else:
            flash('Invalid email or password')
    return render_template('security/login.html', form=form)

# ====================
# ========== sign up
@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = RegisterForm()

    # for select2 fields
    colleges = College.query.all()
    buildings = Building.query.all()

    # query all rooms in database for selectfield
    form.room_id.choices = [(str(room.id), repr(room)) for room in Room.query.all()]

    if form.validate_on_submit():
        hashed_password = utils.encrypt_password(form.password.data)

        first_name = form.first_name.data
        last_name =  form.last_name.data
        email = form.email.data
        password = hashed_password

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        relationship = ResidentOf()
        relationship.user_id = user.id
        if form.room_id.data != "Room":
            relationship.room_id = form.room_id.data
        else:
            relationship.room_id = None

        db.session.add(relationship)
        db.session.commit()

        flash("Welcome, " + form.email.data, 'success')
        return redirect(url_for('main.display'))

    return render_template('security/signup.html', form=form, colleges=colleges, buildings=buildings)

# ====================
# ========== building
@app.route('/building/<int:college_id>')
def building(college_id):
    buildings = Building.query.filter_by(college_id=college_id).all()

    buildingsArray = []

    for building in buildings:
        buildingObj = {}
        buildingObj['id'] = building.id
        buildingObj['name'] = building.name
        buildingsArray.append(buildingObj)
    
    return jsonify({'buildings' : buildingsArray})

# ====================
# ========== room
@app.route('/room/<int:building_id>')
def room(building_id):
    rooms = Room.query.filter_by(building_id=building_id).all()

    roomsArray = []

    for room in rooms:
        roomObj = {}
        roomObj['id'] = room.id
        roomObj['room_number'] = room.room_number
        roomsArray.append(roomObj)
    
    return jsonify({'rooms' : roomsArray})

# ====================
# ========== logout
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ====================
# ========== about
@app.route('/about/')
def about():
    return render_template('stem/about.html')

# ====================
# ========== for dynamic data
# for dynamic site data
# ''' returns room object for use in js functions to render dynamic site data '''
@app.route('/selected_room/<int:room_id>')
def selected_room(room_id):
    # check room_id
    print('room_id: ' + str(room_id))

    # query selected room
    selected_room = Room.query.filter_by(id=room_id).first_or_404()
    building = Building.query.filter_by(id=selected_room.building_id).first_or_404()
    college = College.query.filter_by(id=building.college_id).first_or_404()



    # add room data
    room_data = { 
        # college + building
        'building_name': building.name,
        'address': college.address,
        'site': college.website,
        'floorplan': college.floor_plan,
        'internet': building.internet,
        'desc': building.description,

        # room
        'id': selected_room.id, 
        'number': selected_room.room_number,
        'capacity': selected_room.capacity,
        'xml_path': selected_room.xml_path,
        'gender': selected_room.gender,
        'ac': selected_room.ac,
        'heating': selected_room.heating,
        
        'outlet_count': selected_room.outlet_count,
        'mirror_count': selected_room.mirror_count,
        'drawer_count': selected_room.drawer_count,
        'closet_count': selected_room.closet_count,
        'shelf_count': selected_room.shelf_count,

        'outlet_total': selected_room.outlet_total,
        'mirror_total': selected_room.mirror_total,
        'drawer_total': selected_room.drawer_total,
        'closet_total': selected_room.closet_total,
        'shelf_total': selected_room.shelf_total,

        'full_dims': selected_room.full_dims,
        'bed_dims': selected_room.bed_dims,
        'desk_dims': selected_room.desk_dims,
        'carpet_dims': selected_room.carpet_dims,
        'shelf_dims': selected_room.shelf_dims,
        'closet_dims': selected_room.closet_dims,

        'to_grocery': selected_room.to_grocery,
        'to_gym': selected_room.to_gym,
        'to_hall': selected_room.to_hall,

        'fridge': selected_room.fridge,
        'toaster': selected_room.toaster,
        'coffee': selected_room.coffee,
        'tv': selected_room.tv,

        'img1': selected_room.img1,
        'img2': selected_room.img2,
        'img3': selected_room.img3,
        'img4': selected_room.img4,
        'iframe_src': selected_room.iframe_src
    }
    # check json data
    print ('room_data: ' + json.dumps(room_data, indent=1))

    return jsonify(room_data)

# ====================
# ========== linked room
@app.route('/linked_room/<int:user_id>')
def linked_room(user_id):
    linked_room = ResidentOf.query.filter_by(user_id=user_id).first_or_404()
    room = Room.query.filter_by(id=linked_room.room_id).first_or_404()

    linked_room_data = {
        'linked_xml': room.xml_path
    }

    return jsonify(linked_room_data)

# ====================
# ========== dean panel
@app.route('/deanpanel/')
@roles_required('dean')
def dean_panel():
    all_students = User.query.filter_by(student=True).all()
    all_parents = User.query.filter_by(parent=True).all()
    all_deans = User.query.filter_by(dean=True).all()
    all_users = all_students + all_parents + all_deans
    name = current_user.first_name
    return render_template('stem/dean_panel.html', name=name, users=all_users)

# ====================
# ========== add student
@app.route('/addstudent/', methods=('GET', 'POST'))
@roles_required('dean')
def add_student():
    form = AddStudentForm()
    name = current_user.first_name

    # for select2 fields
    colleges = College.query.all()
    buildings = Building.query.all()

    # query all rooms in database for selectfield
    form.room_id.choices = [(str(room.id), repr(room)) for room in Room.query.all()]

    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name =  form.last_name.data
        email = form.email.data
        password = form.password.data
        student = form.student.data
        parent = form.parent.data
        dean = form.dean.data

        confirmed_at = datetime.utcnow()

        user = User(first_name=first_name, last_name=last_name, email=email, password=password, student=student, parent=parent, dean=dean, confirmed_at=confirmed_at)
        db.session.add(user)
        db.session.commit()


        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        if user.student == True:
            user_datastore.add_role_to_user(user.email, 'student')
        elif user.parent == True:
            user_datastore.add_role_to_user(user.email, 'parent')
        elif user.dean == True:
            user_datastore.add_role_to_user(user.email, 'dean')
        else: 
            flash("You must select a role", 'success')
            return redirect(url_for('main.dean_panel'))

        db.session.commit()

        
        relationship = ResidentOf()
        relationship.user_id = user.id
        if form.room_id.data != "Room":
            relationship.room_id = form.room_id.data
        else:
            relationship.room_id = None

        db.session.add(relationship)
        db.session.commit()

        flash("Added " + form.first_name.data + " " + form.last_name.data, 'success')
        return redirect(url_for('main.dean_panel'))

    return render_template('stem/add_student.html', form=form, colleges=colleges, buildings=buildings, name=name, action="new")

# ====================
# ========== delete user
@app.route('/user/delete/<int:user_id>')
@roles_required('dean')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash("User " + user.first_name + " " + user.last_name + " deleted", 'success')
    return redirect(url_for('main.dean_panel'))

# ====================
# ========== contact
@app.route('/contact/', methods=('GET', 'POST'))
def contact():
    form = ContactForm()

    if form.validate_on_submit():

        # build an email using invoice template and send to invoice recepient
        msg = Message(subject="Note from " + form.full_name.data + "!",
                    sender=form.email.data, 
                    recipients=[private.ADMIN_EMAIL], 
                    body="From " + form.email.data + ", message: " + form.message.data)
        mail.send(msg)

        flash("Your message has been sent. Thank you!", 'success')
        return redirect(url_for('main.index', form=form))

#### flash message test route
# @app.route('/flash/')
# def flash_message():
#     flash("This is a flashed message to help with styling and other needs", 'success')
#     return redirect(url_for('main.display'))
