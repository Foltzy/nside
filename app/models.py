# models.py
from flask_security import UserMixin, RoleMixin, current_user
from datetime import datetime
from flask_admin.contrib import sqla
from . import db 

# create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# customized Role model for sql admin
class PostAdmin(sqla.ModelView):

    # prevent administration of roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

# customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

# role > user
class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String(155))
    last_name = db.Column(db.String(155))
    password = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    dob = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    roles = db.relationship(
        'Role',
        secondary=roles_users
    )

    def __repr__(self):
        if self.first_name:
            return self.first_name
        else:
            return "User ID: #%d" % self.id
    
    def __str__(self):
        return self.__repr__()

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    # many-to-many relationships
    rooms = db.relationship("ResidentOf", back_populates="user")

# college > building > room
class College(db.Model):
    __tablename__ = 'college'
    """
    A user can either be tied to a college or not. 
    Note: This should not infringe on what rooms they can view.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.Text)
    website = db.Column(db.String(120)) 

    # dynamic site data (college)
    floor_plan = db.Column(db.String()) # link
    # /dynamic site data

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return "College ID: #%d" % self.id
    
    def __str__(self):
        return self.__repr__()

    # one-to-many relationships
    buildings = db.relationship('Building', backref='college')

class Building(db.Model):
    __tablename__ = 'building'
    """
    A user can either be tied to a building or not.
    Note: This should not infringe on what rooms they can view.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.Text)
    # foreign key for 'buildings'
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))

    # dynamic site data (building)
    description = db.Column(db.Text)
    internet = db.Column(db.String())
    # /dynamic site data

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return "Building ID: #%d" % self.id
    
    def __str__(self):
        return self.__repr__()

    # one-to-many relationships
    rooms = db.relationship('Room', backref='building')

class Room(db.Model):
    __tablename__ = 'room'
    """
    A user can either be tied to a room or not.
    Note: This should not infringe on what rooms they can view.
    """
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True)
    # foreign key for 'rooms'
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

    # dynamic site data (room)
    capacity = db.Column(db.Integer)
    # xml file path
    xml_path = db.Column(db.String()) # format = 'folder_name/folder_name.xml' no quotes
    # count/totals
    outlet_count = db.Column(db.Integer)
    mirror_count = db.Column(db.Integer)
    drawer_count = db.Column(db.Integer)
    closet_count = db.Column(db.Integer)
    shelf_count = db.Column(db.Integer)
    # dimensions (dims)
    full_dims = db.Column(db.String())
    bed_dims = db.Column(db.String())
    desk_dims = db.Column(db.String())
    carpet_dims = db.Column(db.String())
    shelf_dims = db.Column(db.String())
    closet_dims = db.Column(db.String())
    # commute times
    to_grocery = db.Column(db.String())
    to_gym = db.Column(db.String())
    to_hall = db.Column(db.String()) # to nearest dining hall
    # provided by college
    fridge = db.Column(db.String())
    toaster = db.Column(db.String())
    coffee = db.Column(db.String())
    tv = db.Column(db.String())
    # images and iframe src
    img1 = db.Column(db.String()) # format = 'folder_img/img_name.img_type' no quotes
    img2 = db.Column(db.String())
    img3 = db.Column(db.String())
    img4 = db.Column(db.String())
    iframe_src = db.Column(db.String()) # goes within the src tag... format = just link
    # /dynamic site data

    def __repr__(self):
        if self.room_number:
            return str(self.room_number)
        else:
            return "Room ID: #%d" % self.id
    
    def __str__(self):
        return str(repr(self))

    # many-to-many relationships
    residents = db.relationship("ResidentOf", back_populates="room")

class ResidentOf(db.Model):
    __tablename__ = 'residentof'
    """
    connects a room to a user
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)

    # relationships
    user = db.relationship("User", back_populates="rooms")
    room = db.relationship("Room", back_populates="residents")

    def __repr__(self):
        return "%r's resident, %r" % (self.room, self.user)
    
    def __str__(self):
        r = "null repr"
        try:
            r = str(repr(self))
        except:
            pass
        return r




