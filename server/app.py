import os
import datetime
import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from apscheduler.schedulers.background import BackgroundScheduler
from modules import moisture_sensors, watering, currentstate
from forms import FileNameForm, SeedSelection

# # Initial Flask-Setup
app = Flask(__name__)
nav = Nav()
nav.init_app(app)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
scheduler = BackgroundScheduler()

# # Init sensor modules and relais
thr_sensor = moisture_sensors.ThreadedSensor()
relais_obj = watering.relais()
if os.name != 'nt':
    relais_obj.initialize()
state_obj = currentstate.CurrentState()

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():

    form = FileNameForm()
    if form.validate_on_submit():
        state_obj.change_filename(form.filename.data)

        return redirect(url_for('index'))

    if os.name != 'nt':
        sensor = moisture_sensors.sensor()
        state_obj.moistureString = str(sensor.readI2c())
    else:
        state_obj.moistureString = "Dummy"

    # div = create_figure()
    templateData = {
        'title': 'moisture sensor',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'moisture': state_obj.moistureString,
        'running': state_obj.running,
        'filename': state_obj.filename,
        # 'div1': div,
        'form': form
    }
    if os.name != 'nt':
        del sensor
    return render_template('index.html', **templateData)

@app.route("/plants", methods=["GET", "POST"])
def plants():
    SeedSelectionForm = SeedSelection()
    if SeedSelectionForm.validate_on_submit():
        kwargs = {
            "row1": SeedSelectionForm.row1.data,
            "row2": SeedSelectionForm.row2.data,
            "row3": SeedSelectionForm.row3.data,
            "row4": SeedSelectionForm.row4.data
        }
        state_obj.change_seed_selection(kwargs)
        return redirect(url_for('plants'))

    SeedSelectionForm.row1.default = state_obj.get_seed(row=1)
    SeedSelectionForm.row2.default = state_obj.get_seed(row=2)
    SeedSelectionForm.row3.default = state_obj.get_seed(row=3)
    SeedSelectionForm.row4.default = state_obj.get_seed(row=4)
    SeedSelectionForm.process()

    templateData = {
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'running': state_obj.running,
        'seedselectionform': SeedSelectionForm
    }
    return render_template('set_plants.html', **templateData)

@app.route("/insights")
def insights():
    templateData = {
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'running': state_obj.running,
        'nav': Nav
    }
    return render_template('insights.html', **templateData)

@app.route("/<action>")
def logAction(action):
    logPath = os.path.join("/home/marius/smart_garden/logs/", (state_obj.filename + ".txt"))

    if action == "start":
        try:
            thr_sensor.start(logPath)
            state_obj.running = 1
        except:
            state_obj.running = 0

    elif action == "stop":
        try:
            thr_sensor.stop()
            state_obj.running = 0
        except:
            state_obj.running = 1

    return redirect(url_for('index'))

@app.route("/toggle/<seconds>")
def toggleWater(seconds):
    if int(seconds) < 10:
        relais_obj.toggleFor(int(seconds))

    return redirect(url_for('index'))

def jobEveryXX():
    print('minutely job for testing')

if __name__ == "__main__":
    # # Init scheduler - > Add jobs for watering
    job = scheduler.add_job(jobEveryXX(), 'interval', minutes=1)
    scheduler.start()

    # start app
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
