from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from modules import moisture_sensors
from modules import watering
import plotly
import plotly.graph_objs as go
import json
import datetime
import os
import random

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

def create_figure():
    count = 25
    xScale = [i for i in range(0,count)]
    yScale = [random.randint(135, 213)  for i in range(0,count)]

    # Create a trace
    trace = go.Scatter(x=xScale, y=yScale)
    fig = go.Figure(trace)
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)

    return div

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():

    form = FileNameForm()
    if form.validate_on_submit():
        s.filename = form.filename.data
        return redirect(url_for('index'))

    sensor = moisture_sensors.sensor()
    s.moistureString = str(sensor.readI2c())

    div  = create_figure()
    templateData = {
        'title': 'moisture sensor',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'moisture': s.moistureString,
        'running': s.running,
        'filename': s.filename,
        'div1': div,
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

@app.route("/<action>")
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

    return redirect(url_for('index'))

@app.route("/toggle/<seconds>")
def toggleWater(seconds):
    if int(seconds) < 10:
        r.toggleFor(int(seconds))

    return redirect(url_for('index'))

if __name__ == "__main__":
    t = moisture_sensors.ThreadedSensor()
    r = watering.relais()
    r.initialize()
    s = state()
    # start app
    app.run(host='0.0.0.0', port=8080, debug=True)
