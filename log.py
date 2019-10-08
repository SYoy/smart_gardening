from sensors import moisture_sensors
import time
import datetime

sensor = moisture_sensors.sensor()

while True:
    if 0xFF == ord("q"):
        break
    val = sensor.readI2c()

    with open("testlog_2.txt", "a") as myfile:
        myfile.write(datetime.datetime.now().strftime("%H:%M:%S")+" - " + str(val)+"\n")

    time.sleep(3)
