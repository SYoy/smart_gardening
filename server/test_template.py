from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from sensors import moisture_sensors
import datetime
import os

log_name = "default.txt"
app = Flask(__name__)
Bootstrap(app)
moistureString = "?"
running = 0


@app.route("/")
def index():
    sensor = moisture_sensors.sensor()
    moistureString = str(sensor.readI2c())
    templateData = {
        'title': 'moisture sensor',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'moisture': moistureString,
        'running': running
    }
    del sensor
    return render_template('index.html', **templateData)


@app.route("/ms/<action>")
def logAction(action):
    logPath = os.path.join("/home/marius/smart_garden/logs/", log_name)

    if action == "start":
        try:
            t.start(logPath)
            running = 1
        except:
            running = 0

    elif action == "stop":
        try:
            t.stop()
            running = 0
        except:
            running = 1

    templateData = {
        'title': 'moisture sensor',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'moisture': moistureString,
        'running': running
    }

    return render_template('index.html', **templateData)


if __name__ == "__main__":
    t = moisture_sensors.ThreadedSensor()
    app.run(host='0.0.0.0', port=1080, debug=True)
