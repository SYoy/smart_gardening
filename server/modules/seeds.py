import os
import json
import datetime


available_seedclasses = ["universal", "tomato_dummy", "ginger_dummy"]


def get_seed_class_obj(arg):
    if arg in ["universal", 0, "universal_seed", "un", "default", None]:
        instance = universal_seed()
        return instance
    elif arg in []:
        exit()


class universal_seed():
    def __init__(self):
        self.water_every_X_hours = 10
        self.seed = "universal"
        self.amount = 1

    def toDict(self):
        dict = {
            "water_every_X_hours": self.water_every_X_hours,
            "seed": self.seed
        }
        return dict


    def check_watering_status(self, lt_watered_string):
        """
        color - 5 levels - 0 good 5 bad
        water_now: bool -> water immediately
        """
        lt_watered_datetime = datetime.datetime.strptime(lt_watered_string, "%m-%d-%Y-%H:%M:%S")
        now = datetime.datetime.now()

        delta = now - lt_watered_datetime
        dt_hours = delta.days * 24 + delta.seconds / 60 / 60

        if dt_hours > self.water_every_X_hours:
            water_now = True
            color = self.estimate_watering_level(dt_hours/self.water_every_X_hours)
        else:
            water_now = False
            color = self.estimate_watering_level(dt_hours/self.water_every_X_hours)

        return water_now, self.amount, color


    def estimate_watering_level(self, factor):
        if factor < 0.2:
            return 1
        elif factor < 0.4:
            return 2
        elif factor < 0.6:
            return 3
        elif factor < 0.8:
            return 4
        return 5


class tomato_dummy(universal_seed):
    def __init__(self):
        self.water_every_X_hours = 36
        self.seed = "tomato_dummy"
        self.amount = 2

class ginger_dummy(universal_seed):
    def __init__(self):
        self.water_every_X_hours = 6
        self.seed = "ginger_dummy"
        self.amount = 0.5

# # Todo: - Trigger Watering - log Watering