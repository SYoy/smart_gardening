import RPi.GPIO as GPIO
import time

class relais():
    def __init__(self):
        self.gpio = 10

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.LOW)
        self.status = 0

    def toggle(self):
        if self.status:
            GPIO.output(self.gpio, GPIO.LOW)
        elif not self.status:
            GPIO.output(self.gpio, GPIO.HIGH)

    def toggleFor(self, seconds):
        self.toggle()
        time.sleep(seconds)
        self.toggle()

    def close(self):
        GPIO.cleanup()