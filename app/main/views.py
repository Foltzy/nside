# views.py
from flask import Flask, request, render_template, flash, redirect, \
    url_for, jsonify, current_app
from flask_security import current_user, utils
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# files
from .forms import LoginForm, RegisterForm, ResidentOfForm
from . import main as app
from .. import db
from ..models import College, Building, Room, ResidentOf, User

import json

@app.route('/')
@app.route('/index/')
def index():
    return render_template('stem/index.html')

@app.route('/display/')
@login_required
def display():
    # select2 field queries
    colleges = College.query.all()
    buildings = Building.query.all()
    all_rooms = Room.query.all()

    name = current_user.first_name

    # see if the  user is linked  to a room if not set to 'None'
    if len(current_user.rooms) != 0:
        linked_room = current_user.rooms[0]
    else:
        linked_room = None

    return render_template('stem/display.html', name=name, linked_room=linked_room, colleges=colleges, buildings=buildings, rooms=all_rooms)

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

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@app.route('/new_link/', methods=('GET', 'POST'))
@login_required
def new_link():
    form = ResidentOfForm()
    # for select2 fields
    colleges = College.query.all()
    buildings = Building.query.all()

    # query all rooms in database for selectfield
    form.room_id.choices = [(str(room.id), repr(room)) for room in Room.query.all()]

    if form.validate_on_submit():
        relationship = ResidentOf()
        relationship.user_id = current_user.id
        relationship.room_id = form.room_id.data
        db.session.add(relationship)
        db.session.commit()

        new_room = Room.query.filter_by(id=form.room_id.data).first_or_404()

        flash("You are now linked to " + str(new_room), 'success')
        return redirect(url_for('main.display'))
    
    return render_template('stem/residentof_form.html', form=form, colleges=colleges, buildings=buildings, action="new")

@app.route('/edit_link/<int:residentof_id>', methods=('GET', 'POST'))
@login_required
def edit_link(residentof_id):
    # for select2 fields
    colleges = College.query.all()
    buildings = Building.query.all()
    residentof = ResidentOf.query.filter_by(id=residentof_id).first_or_404()
    form = ResidentOfForm()

    form = ResidentOfForm(obj=residentof)

    # query all rooms in database for selectfield
    form.room_id.choices = [(str(room.id), repr(room)) for room in Room.query.all()]

    if form.validate_on_submit():
        form.populate_obj(residentof)

        room_id = residentof.room_id
        db.session.commit()

        flash("Link updated", 'success')
        return redirect(url_for('main.display'))
    
    return render_template('stem/residentof_form.html', form=form, colleges=colleges, buildings=buildings, residentof=residentof, action="edit")

@app.route('/about/')
def about():
    return render_template('stem/about.html')

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
        
        'outlet_count': selected_room.outlet_count,
        'mirror_count': selected_room.mirror_count,
        'drawer_count': selected_room.drawer_count,
        'closet_count': selected_room.closet_count,
        'shelf_count': selected_room.shelf_count,

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

@app.route('/linked_room/<int:user_id>')
def linked_room(user_id):
    linked_room = ResidentOf.query.filter_by(user_id=user_id).first_or_404()
    room = Room.query.filter_by(id=linked_room.room_id).first_or_404()

    linked_room_data = {
        'linked_xml': room.xml_path
    }

    return jsonify(linked_room_data)





