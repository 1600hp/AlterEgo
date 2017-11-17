import asyncio
import re
from datetime import datetime

from conversation import Conversation
from discord_utils import slow_send
from croissant.calendar import Calendar

class EventPlanner(Conversation):
    def __init__(self, client, author, calendar):
        self.author = author
        self.calendar = calendar
        self.client = client
        self.state = 0
        self.asking_days = False

        self.full_date = re.compile("[0-9]+/[0-9]+/[0-9]+")
        self.part_date = re.compile("[0-9]+/[0-9]+")

        self.name = ""
        self.description = ""
        self.repeat = Calendar.RepeatType.NONE
        self.repeat_indices = []
        self.start_date = "01/01/1970"
        self.end_date = ""

    def _reject(self, tokens):
        return tokens in [["no"], ["nope"], ["n"], ["none"]]

    def _pull_date(self, text):
        found = re.search(self.full_date, text)
        if found:
            return text[found.span()[0]:found.span()[1]]

        found = re.search(self.part_date, text)
        if found:
            return text[found.span()[0]:found.span()[1]] + str(datetime.now().year)[:2]

        return None

    @asyncio.coroutine
    def expected_next(self, msg, **kwargs):
        return msg.channel.is_private and msg.channel.user == self.author

    @asyncio.coroutine
    def apply(self, msg, tokens=[], **kwargs):
        if self.asking_days:
            if "sun" in tokens or "sunday" in tokens:
                self.repeat_indices.append(0)
            if "mon" in tokens or "monday" in tokens:
                self.repeat_indices.append(1)
            if "tues" in tokens or "tuesday" in tokens:
                self.repeat_indices.append(2)
            if "wed" in tokens or "wednesday" in tokens:
                self.repeat_indices.append(3)
            if "thurs" in tokens or "thursday" in tokens:
                self.repeat_indices.append(4)
            if "fri" in tokens or "friday" in tokens:
                self.repeat_indices.append(5)
            if "sat" in tokens or "saturday" in tokens:
                self.repeat_indices.append(6)

            if not len(self.repeat_indices):
                yield from self.slow_send(self.client, self.author, 
                        "Sorry, I didn't catch that.  On what days would you like your event to occur?")
                return False

            yield from self.slow_send(self.client, self.author,
                    "What date would you like your event to start?")
            self.asking_days = False
            return False

        if self.state == 0:   # Name
            self.name = msg.content
            yield from slow_send(self.client, self.author, 
                    "Would you like to give your event a description?")

        elif self.state == 1: # Description
            if not self._reject(tokens):
                self.description = msg.content
            yield from slow_send(self.client, self.author, 
                    "Would you like your event to repeat?  If so, how often?")

        elif self.state == 2: # Repeat Type
            if not self._reject(tokens):
                if "daily" or "day" in tokens:
                    self.repeat = Calendar.RepeatType.WEEKLY
                    self.repeat_indices = [0, 1, 2, 3, 4, 5, 6]
                elif "weekly" or "week" in tokens:
                    self.repeat = Calendar.RepeatType.WEEKLY
                    self.asking_days = True
                elif "monthly" or "month" in tokens:
                    self.repeat = Calendar.RepeatType.MONTHLY
                elif "yearly" or "year" in tokens:
                    self.repeat = Calendar.RepeatType.YEARLY

                if self.asking_days:
                    yield from slow_send(self.client, self.author,
                            "What day(s) of the week will your event occur?")
                else:
                    yield from slow_send(self.client, self.author,
                            "What date would you like your event to start?")
            else: # No repeat
                yield from slow_send(self.client, self.author, "What date would you like your event to be?")

        elif self.state == 3: # Start Date
            date = self._pull_date(msg.content)
            if not date:
                yield from slow_send(self.client, self.author, 
                        "Sorry, didn't catch that... I need a date in M/D/Y format.")
                return False

            self.start_date = date

            if self.repeat != Calendar.RepeatType.NONE:
                yield from slow_send(self.client, self.author,
                        "Would you like to set an end date?  If so, what date?")
            else:
                self.state += 1 # Skip the end date
                yield from slow_send(self.client, self.author,
                        "Okay, event set.")

        elif self.state == 4: # End Date
            date = self._pull_date(msg.content)
            if date:
                self.end_date = date
            yield from slow_send(self.client, self.author,
                    "Okay, event set.")


        elif self.state == 5: # Start Time
            pass
        elif self.state == 6: # End Time
            pass
        elif self.state == 7: # Location
            pass

        self.state += 1
        if self.state > 4:
            self.calendar.add_event(
                    self.name,
                    description=self.description,
                    repeat_type=self.repeat,
                    repeat_indices=self.repeat_indices,
                    start_date=self.start_date,
                    end_date=self.end_date)
            self.calendar.save_file()

        return self.state > 4 # Skipping location and timing for now
            
