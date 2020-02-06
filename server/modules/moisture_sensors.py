import os
import time
import threading
import datetime

if os.name != 'nt':
    import smbus


class sensor(object):

    def __init__(self, add=0x48, port_in=0x02):
        self.i2c_address = add  # I2C-Adresse des Wandler
        self.analog_port_in = port_in  # Sensor-Standard
        self.i2c = smbus.SMBus(1)  # 2C-Instanz

    def readI2c(self):
        _ = self.i2c.read_byte_data(self.i2c_address,
                                    self.analog_port_in)  # placeholder und neuen Wert generieren aus Speicher
        time.sleep(0.01)
        val = self.i2c.read_byte_data(self.i2c_address,
                                      self.analog_port_in)  # aktueller Wert aus Speicher - zeitpunkt erste Abfrage
        return val

    def writeI2c(self, i2cDeviceAddr, channel, value):
        #    self.i2c.write_byte_data(i2cDeviceAddr, 0x40 + channel, value)
        print("not implemented yet")


class ThreadedSensor(object):

    def __init__(self, intervall=10):
        self.interval = intervall
        self._stop = False

    def start(self, logpath):
        self.logpath = logpath
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def stop(self):
        self._stop = True

    def run(self):
        """ Method that runs forever """
        s = sensor()
        while not self._stop == True:
            _ = s.readI2c()
            val = s.readI2c()
            with open(self.logpath, 'a') as file:
                file.write(datetime.datetime.now().strftime("%H:%M:%S") + ', ' + str(val) + ' \n')
            time.sleep(self.interval)
        with open(self.logpath, 'a') as file:
            file.write(datetime.datetime.now().strftime("%H:%M:%S") + ', ' + 'closed' + ' \n')
