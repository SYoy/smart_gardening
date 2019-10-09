from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from sensors import moisture_sensors
import datetime
import os

#flask setup
app = Flask(__name__)
nav = Nav()
nav.init_app(app)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class state():
    def __init__(self):
        self.moistureString = "?"
        self.running = 0
        self.filename = "default"

class FileNameForm(FlaskForm):
    filename = StringField('new filename:', validators=[DataRequired()])
    submit = SubmitField('change filename')

@app.route("/")
@app.route("/index")
@app.route('/filename', methods=['GET', 'POST'])
def index():

    form = FileNameForm()
    if form.validate_on_submit():
        s.filename = form.filename.data
        # templateData = {
        #     'title': 'moisture sensor',
        #     'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        #     'moisture': s.moistureString,
        #     'running': s.running,
        #     'filename': s.filename,
        #     'form': form
        # }

        return redirect(url_for('index', **templateData))

    sensor = moisture_sensors.sensor()
    s.moistureString = str(sensor.readI2c())
    templateData = {
        'title': 'moisture sensor',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'moisture': s.moistureString,
        'running': s.running,
        'filename': s.filename,
        'form': form
    }
    del sensor
    return render_template('index_sp.html', **templateData)

@app.route("/insights")
def insights():
    templateData = {
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'running': s.running
    }
    return render_template('insights.html', **templateData)

@app.route("/ms/<action>")
def logAction(action):
    logPath = os.path.join("/home/marius/smart_garden/logs/", (s.filename+".txt"))

    if action == "start":
        try:
            t.start(logPath)
            s.running = 1
        except:
            s.running = 0

    elif action == "stop":
        try:
            t.stop()
            s.running = 0
        except:
            s.running = 1

    # form = FileNameForm()
    # templateData = {
    #     'title': 'moisture sensor',
    #     'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    #     'moisture': s.moistureString,
    #     'running': s.running,
    #     'filename': s.filename,
    #     'form': form
    # }

    return redirect(url_for('index', **templateData))

if __name__ == "__main__":
    t = moisture_sensors.ThreadedSensor()
    s = state()
    # start app
    app.run(host='0.0.0.0', port=1080, debug=True)
