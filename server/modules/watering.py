import os
import time

if os.name != 'nt':
    import RPi.GPIO as GPIO

class relais():
    def __init__(self, num=1):
        #TODO GPIO num for other Relais
        if num == 1:
            self.gpio = 10
        elif num == 2:
            self.gpio = 101
        elif num == 3:
            self.gpio = 102
        elif num == 5:
            self.gpio = 103

    def initialize(self):
        try:
            GPIO.cleanup()
        except:
            pass
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.HIGH)
        self.status = 0

    def toggle(self):
        if self.status:
            GPIO.output(self.gpio, GPIO.HIGH)
            self.status = 0
        elif not self.status:
            GPIO.output(self.gpio, GPIO.LOW)
            self.status = 1

    def toggleFor(self, seconds):
        self.toggle()
        time.sleep(seconds)
        self.toggle()

    def close(self):
        GPIO.cleanup()