import random
import string
from datetime import datetime, timedelta
from date_time_utils import get_date, get_time, hour_rounder
from event import TimedEvent, AllDayEvent


class EventCreate:
    def __init__(self):
        self.date_today = datetime.now()
        self.round_hour = hour_rounder(self.date_today)
        self.event_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def event_constructor(self, events_dict):
        event_name: str = input("Enter event name: ")
        event_description: str = input("Enter event description. If none, press enter: ") or "No description given."
        event_all_day: str or bool = input("Is this an all day event? ").lower() or "no"
        event_start_date = get_date("Enter start date (MM-DD-YYYY): ") or self.date_today.date()
        event_end_date = get_date("Enter end date (MM-DD-YYYY): ") or self.date_today.date()

        if event_all_day == "no":
            event_data = self.create_timed_event(self.event_id, event_name, event_description,
                                                 event_start_date, event_end_date)
        else:
            event_data = self.create_all_day_event(self.event_id, event_name, event_description,
                                                   event_start_date, event_end_date)

        if event_start_date not in events_dict:
            events_dict[event_start_date] = {}

        events_dict[event_start_date][self.event_id] = event_data

        print(f"Event '{event_name}' with ID '{self.event_id}' was added successfully!")

        return events_dict

    def create_all_day_event(self, event_id, event_name, event_description, event_start_date,
                             event_end_date):
        event_all_day = True
        return AllDayEvent(event_id, event_name, event_description,
                           event_all_day, event_start_date, event_end_date)

    def create_timed_event(self, event_id, event_name, event_description, event_start_date, event_end_date):

        event_all_day = False
        event_start_time = get_time("Enter start time (24-hour format): ") or self.round_hour
        event_end_time = get_time("Enter end time (24-hour format): ") or self.round_hour + timedelta(hours=1)

        # if event_start_time > event_start_date: event_start_date = event_start_time.date()
        # if event_end_time > event_end_date: event_end_date = event_end_time.date()

        return TimedEvent(event_id, event_name, event_description,
                          event_all_day, event_start_date, event_end_date,
                          event_start_time, event_end_time)
