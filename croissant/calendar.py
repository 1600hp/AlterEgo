import json
import os

from datetime import date, time
from functools import reduce

class Calendar:
    calendar = []
    fname = None

    class RepeatType:
        NONE = 0
        WEEKLY = 1
        MONTHLY = 2
        YEARLY = 3

    def __init__(self, fname=None):
        if fname: self.fname = fname
        if fname and os.path.exists(fname):
            with open(fname, 'r') as fp:
                self.calendar = json.load(fp)

    def load_file(self, fname):
        self.fname = fname
        if os.path.exists(fname):
            with open(fname, 'r') as fp:
                self.calendar = json.load(fp)

    def save_file(self, fname=None):
        if not fname: fname = self.fname

        with open(fname, 'w') as fp:
            json.dump(self.calendar, fp)

    def get_next_id(self):
        return reduce(lambda x, y: max(x, y), self.calendar, 0) + 1

    def add_event(self,
            name, 
            description="", 
            repeat_type=0,
            repeat_indices=[],
            start_date="",
            end_date="",
            start_time="",
            end_time="",
            location="",
            attendees=[]):
        next_id = self.get_next_id()
        event = {
                "id":next_id,
                "name":name,
                "description":description,
                "repeat":repeat_type,
                "repeat_index":repeat_indices,
                "start_date":start_date,
                "end_date":end_date,
                "start_time":start_time,
                "end_time":end_time,
                "location":location,
                "attendees":attendees
                }
        self.calendar.append(event)

    def remove_event(self, id_num):
        self.calendar = filter(lambda x: x["id"] != id_num, self.calendar)

    def day_in_range(self, event, date):
        event_start = event["start_date"].split("/")
        event_end = event["end_date"].split("/")
        event_start = date(event_start[2], event_end[0], event_end[1])
        event_end = date(event_end[2], event_end[0], event_end[1])
        return event_start <= date and date <= event_end

    def events_in_range(self, date):
        return filter(lambda x: day_in_range(x, date), self.events)

    def get_by_name(self, name):
        return filter(lambda x: x["name"] == name, self.events)
