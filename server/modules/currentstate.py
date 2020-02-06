import os
import json
import datetime

from seeds import available_seedclasses

class CurrentState():
    def __init__(self):
        self.moistureString = "?"
        self.running = "0"
        self.path_savedir = os.path.abspath(os.path.join(os.path.basename(__file__), "../server/savedir"))

        if os.path.isfile(os.path.join(self.path_savedir, "current_selection.json")):
            with open(os.path.join(self.path_savedir, "current_selection.json"), "r") as f:
                self.current_selection = json.load(f)
            try:
                savedate = self.current_selection["savedate"]
            except:
                savedate = None

            print("[Current State] Loaded and Initialized state from: ", savedate)
        else:
            print("[Current State] No current selection found in: ", os.path.join(self.path_savedir, "current_selection.json"))
            exit()

        self.filename = self.current_selection["filename"]
        self.num_rows = self.current_selection["num_rows"]


    def save_current_state(self):
        with open(os.path.join(self.path_savedir, "current_selection.json"), "w") as f:
            self.current_selection["savedate"] = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
            json.dump(self.current_selection, f)


    def change_filename(self, name):
        self.filename = name
        self.current_selection["filename"] = name

        self.save_current_state()


    def change_seed_selection(self, dict):
        for key, value in dict.items():
            self.current_selection["selection"][key]["seedclass"] = value

        self.save_current_state()


    def log_watering_row(self, *row):
        map = {
            1: "row1",
            2: "row2",
            3: "row3",
            4: "row4",
        }
        for r in row:
            self.current_selection["selection"][map[r]]["last_time_watered"] = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")

        self.save_current_state()

    def get_seed(self, row):
        map = {
            1: "row1",
            2: "row2",
            3: "row3",
            4: "row4",
        }
        if self.current_selection["selection"][map[row]]["seedclass"] in available_seedclasses:
            return self.current_selection["selection"][map[row]]["seedclass"]
        else:
            return "universal"
