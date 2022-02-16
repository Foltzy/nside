                 _                   _               _            _            _      
                / /\                / /\            /\ \         /\ \         /\ \    
               / /  \              / /  \          /  \ \       /  \ \____   /  \ \   
              / / /\ \            / / /\ \        / /\ \ \     / /\ \_____\ / /\ \ \  
             / / /\ \ \          / / /\ \ \      / / /\ \ \   / / /\/___  // / /\ \_\ 
            / / /  \ \ \        / / /\ \_\ \    / / /  \ \_\ / / /   / / // /_/_ \/_/ 
           / / /___/ /\ \      / / /\ \ \___\  / / /   / / // / /   / / // /____/\    
          / / /_____/ /\ \    / / /  \ \ \__/ / / /   / / // / /   / / // /\____\/    
         / /_________/\ \ \  / / /____\_\ \  / / /___/ / / \ \ \__/ / // / /______    
        / / /_       __\ \_\/ / /__________\/ / /____\/ /   \ \___\/ // / /_______\   
        \_\___\     /____/_/\/_____________/\/_________/     \/_____/ \/__________/   
        Author: Ben Foltz  |  Advisor: Drew Guarnera  |  Department: Computer Science   
                                                                              
# Abode Interior Documentation

## Independent Study
This documentation is written in accordance to the Senior Independent Study for College of Wooster Computer Science graduates. My independent study is on the research, planning, and creation of this full stack web application and can be found at [IS FINAL LINK](#) and is documented below.

&nbsp;


## Web Application
This project is a full stack web application that utilizes a Flask Micro Framework and PostgreSQL back-end assisted by database technologies like the SQLAlchemy ORM and Jinja2 with a heavy JavaScript, HTML, and CSS based front-end all detailed below. View the final project live at [www.abodeinterior.net](www.abodeinterior.net). Note: an example room is accessible in the navigation menu.    

### Stack
1. Back-end: [Flask Python Micro Framework](https://flask.palletsprojects.com/en/2.0.x/), [PostgreSQL](https://www.postgresql.org/docs/), [SQLAlchemy](https://docs.sqlalchemy.org/en/14/), [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
2. Software components: [Canvas.io](https://canvas.io/), [Canvas Scan to CAD](https://support.canvas.io/article/12-what-is-scan-to-cad), [WebRotate 360](https://www.webrotate360.com/)
3. Front-end: [JavaScript JSON](https://docs.oracle.com/javame/8.0/api/json/api/com/oracle/json/JsonObject.html), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)

### Purpose
Incoming college freshman need to plan ahead. These dedicated, passionate students already have a lot on their plate, and planning for dorm room living is one of these challenges. Most universities don’t have detailed dorm room layouts, leading to confusion and misinformation about how much space is provided and what students actually need to bring along with them. Abode Interior fixes this problem. 

&nbsp;


### Usage
These are the official steps in order to run the Abode web application on a local device and configure the development enviroment. This can be thought of as a "personal copy" of the Abode app and not the live site. A link to the production server can be found above.

&nbsp;

1. Clone the repository from `https://github.com/Foltzy/nside.git`.
2. Stand up the database:
     - There are two files that hold settings for the Abode web application. The first is called the `private.py` and this file is not included in the GitHub repository for security purposes. Thus, this file needs to be created. Below is the exact Abode private file with all required field information removed and marked with large X's, these fields will need to be filled out in order to connect to your local database.
     - *Note: These settings are stored in the `.env` file for production servers as it follows the Flask web application naming conventions and best practices.*  
     ```python
     import os

     # Secret key for site wide encryption, should be long, random, and secure.
     SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

     # Database username, password, and name. Should match PostgreSQL database.
     DB_USERNAME = os.environ.get("DB_USERNAME", 'XXXXXXXX')
     DB_PASSWORD = os.environ.get("DB_PASSWORD", 'XXXXXXXX')
     DATABASE_NAME = os.environ.get("DATABASE_NAME", 'XXXXXXXX')

     # Admin password and email. These settings are used to create an admin user you can login with, and ideally would remain unchanged.  
     STARTING_ADMIN_PASS = 'XXXXXXXX'
     STARTING_ADMIN1 = 'XXXXXXXXXXXXXXXXX'

     # Mail server. Abode utilizes a gmail SMTP server, however if this differs from your set up, the initial settings below will need to be updated.
     MAIL_SERVER = 'smtp.gmail.com'
     MAIL_PORT = 465
     MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
     MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
     MAIL_USERNAME = os.environ.get("MAIL_USERNAME", 'XXXXXXXX')
     MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", 'XXXXXXXX')
     ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", 'XXXXXXXXXXXXXXXXX')

     # Flask-Security hash and salt for encryption. Follow the same practices with the SECRET_KEY setting above. 
     SECURITY_PASSWORD_HASH = 'XXXXXXXX'
     SECURITY_PASSWORD_SALT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
     ```
     - *Note that these settings are to be treated with the utmost security since a malicious user with access to this file gains full control of the web application and database. Including this file in a `.gitignore` is best practice to prevent these attacks.*  
     - The second file is called the `settings.py` and its sole function is to reference the previous file, instantiate these settings, and provide further configuration that does not need external security measures. If you are still confused on the function of these two files take a look at the `settings.py` within this repository.    
3. Double check and finalize the configuration of the `settings.py` file. 
4. Set up the virtual environment:
     - Virtual environments are used to narrow the scope of our dependencies, this way they can only be accessed by our web application, reducing the chances of external interference with other projects.
        - `~$ python3 -m venv venv`
     - We can then activate our virtual environment and install our depenencies.
        - `~$ source venv/bin/activate`
        - `(venv)~$ pip install -r requirements.txt`   
6. Run and test:
     - Test by running `(venv)~$ flask run` 
     - You should now be able to view the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

&nbsp;

## License
- Copyright © Abode, Abode Interior, and Abode Interior Inc. at [abodeinterior.net](https://abodeinterior.net) 2021
- Software licensing is found within the repository, inside the tools assets folder, under the name `license.lic`. All softwares have been purchased and paid for in full or utilize free versions.

&nbsp;

## Version
v1.0.2

